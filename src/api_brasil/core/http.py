"""Cliente HTTP interno da SDK.

Injeta os headers de autenticação da plataforma (``Authorization: Bearer``,
``DeviceToken``, ``SecretKey``), aplica retry com backoff, dispara hooks de
observabilidade e converte falhas em subclasses de ``ApiBrasilError``.
"""

from __future__ import annotations

import json as jsonlib
import time
from typing import Any, Dict, Mapping, Optional, Union
from urllib.parse import quote_plus

from .env import config_from_env
from .errors import (
    ApiBrasilError,
    NetworkError,
    RateLimitError,
    TimeoutError,
    create_api_error,
)
from .retry import backoff_delay_ms, resolve_retry, sleep_ms
from .transport import Transport, TransportRequest, default_transport

__all__ = ["HttpClient", "DEFAULT_BASE_URL", "DEFAULT_TIMEOUT", "SDK_USER_AGENT"]

DEFAULT_BASE_URL = "https://gateway.apibrasil.io/api/v2"
DEFAULT_TIMEOUT = 30000
SDK_USER_AGENT = "APIBRASIL/SDK-PYTHON"

#: Chaves aceitas em ``**options`` (opções por requisição).
REQUEST_OPTION_KEYS = frozenset(
    {
        "query",
        "headers",
        "bearer_token",
        "device_token",
        "secret_key",
        "timeout",
        "response_type",
    }
)

_CONFIG_KEYS = frozenset(
    {
        "bearer_token",
        "device_token",
        "secret_key",
        "base_url",
        "timeout",
        "headers",
        "transport",
        "retry",
        "hooks",
    }
)


class HttpClient:
    """Cliente HTTP interno da SDK.

    Chaves de configuração aceitas:

    - ``bearer_token`` (str): token JWT obtido no login
    - ``device_token`` (str): token do dispositivo (serviços device-based)
    - ``secret_key`` (str): SecretKey da API (usada ao criar devices)
    - ``base_url`` (str): base da API. Padrão: ``https://gateway.apibrasil.io/api/v2``
    - ``timeout`` (int): timeout das requisições em **milissegundos**. Padrão: 30000
    - ``headers`` (dict): headers adicionais em todas as requisições
    - ``transport`` (:class:`~api_brasil.core.transport.Transport`): transporte customizado
    - ``retry`` (dict | False): política de retry — veja ``DEFAULT_RETRY``
    - ``hooks`` (dict): ``on_request``, ``on_response``, ``on_retry`` (callables)

    Opções por requisição (``**options``), que sobrescrevem a configuração:
    ``query``, ``headers``, ``bearer_token``, ``device_token``, ``secret_key``,
    ``timeout``, ``response_type`` (``json`` | ``raw`` | ``text`` | ``stream``).
    """

    DEFAULT_BASE_URL = DEFAULT_BASE_URL
    DEFAULT_TIMEOUT = DEFAULT_TIMEOUT
    SDK_USER_AGENT = SDK_USER_AGENT

    def __init__(
        self, config: Optional[Mapping[str, Any]] = None, **overrides: Any
    ) -> None:
        merged: Dict[str, Any] = dict(config or {})
        merged.update(overrides)

        unknown = set(merged) - _CONFIG_KEYS
        if unknown:
            raise TypeError(
                "Configuração desconhecida: {}. Aceitas: {}.".format(
                    ", ".join(sorted(unknown)), ", ".join(sorted(_CONFIG_KEYS))
                )
            )

        self._config: Dict[str, Any] = dict(config_from_env())
        self._config.update(
            {key: value for key, value in merged.items() if value is not None}
        )

        transport = self._config.get("transport")
        self._transport: Transport = (
            transport if isinstance(transport, Transport) else default_transport()
        )

        self._retry = resolve_retry(self._config.get("retry"))
        hooks = self._config.get("hooks")
        self._hooks: Dict[str, Any] = dict(hooks) if isinstance(hooks, Mapping) else {}

    # ------------------------------------------------------------------
    # Configuração
    # ------------------------------------------------------------------

    @property
    def base_url(self) -> str:
        base_url = self._config.get("base_url")

        return base_url if isinstance(base_url, str) and base_url else DEFAULT_BASE_URL

    @property
    def bearer_token(self) -> Optional[str]:
        token = self._config.get("bearer_token")

        return token if isinstance(token, str) else None

    @property
    def device_token(self) -> Optional[str]:
        token = self._config.get("device_token")

        return token if isinstance(token, str) else None

    @property
    def secret_key(self) -> Optional[str]:
        key = self._config.get("secret_key")

        return key if isinstance(key, str) else None

    @property
    def transport(self) -> Transport:
        return self._transport

    def set_bearer_token(self, token: Optional[str]) -> None:
        """Define/atualiza o Bearer Token do cliente."""
        if token is None:
            self._config.pop("bearer_token", None)
            return

        self._config["bearer_token"] = token

    def set_device_token(self, token: Optional[str]) -> None:
        """Define/atualiza o DeviceToken do cliente."""
        if token is None:
            self._config.pop("device_token", None)
            return

        self._config["device_token"] = token

    def get_config(self) -> Dict[str, Any]:
        """Configuração atual do cliente (útil para clonar com outro device)."""
        config = dict(self._config)
        config["transport"] = self._transport

        return config

    # ------------------------------------------------------------------
    # Requisições
    # ------------------------------------------------------------------

    def request(
        self,
        method: str,
        path: str,
        body: Any = None,
        **options: Any,
    ) -> Any:
        """Executa uma requisição no gateway e devolve o corpo já decodificado."""
        unknown = set(options) - REQUEST_OPTION_KEYS
        if unknown:
            raise TypeError(
                "Opção de requisição desconhecida: {}. Aceitas: {}.".format(
                    ", ".join(sorted(unknown)), ", ".join(sorted(REQUEST_OPTION_KEYS))
                )
            )

        method = method.upper()
        headers = self._build_headers(options)
        url = _join_url(self.base_url, path) + _build_query_string(options.get("query"))
        serialized_body = None if body is None else _encode_body(body)
        timeout_ms = int(
            options.get("timeout") or self._config.get("timeout") or DEFAULT_TIMEOUT
        )
        response_type = options.get("response_type")
        max_attempts = 1 + (self._retry["retries"] if self._retry else 0)

        attempt = 0
        while True:
            self._fire_hook(
                "on_request",
                {
                    "method": method,
                    "url": url,
                    "headers": headers,
                    "body": body,
                    "attempt": attempt,
                },
            )

            started_at = time.monotonic()

            try:
                response = self._transport.request(
                    TransportRequest(
                        method=method,
                        url=url,
                        headers=headers,
                        body=serialized_body,
                        timeout_ms=timeout_ms,
                        response_type=response_type,
                    )
                )
            except Exception as error:  # noqa: BLE001 - normalizado abaixo
                retryable = isinstance(error, NetworkError) and not isinstance(
                    error, TimeoutError
                )

                if retryable and self._retry and attempt + 1 < max_attempts:
                    delay_ms = backoff_delay_ms(attempt, self._retry)
                    attempt += 1
                    self._fire_hook(
                        "on_retry",
                        {
                            "method": method,
                            "url": url,
                            "attempt": attempt,
                            "delay_ms": delay_ms,
                            "reason": str(error),
                        },
                    )
                    sleep_ms(delay_ms)
                    continue

                raise ApiBrasilError.from_exception(error) from error

            self._fire_hook(
                "on_response",
                {
                    "method": method,
                    "url": url,
                    "status": response.status,
                    "duration_ms": int(round((time.monotonic() - started_at) * 1000)),
                    "attempt": attempt,
                },
            )

            if response.status >= 400:
                error = create_api_error(
                    response.status, response.data, response.headers
                )
                retryable_status = (
                    self._retry is not None
                    and response.status in self._retry["retry_on_statuses"]
                )

                if retryable_status and attempt + 1 < max_attempts:
                    if (
                        isinstance(error, RateLimitError)
                        and error.retry_after_ms is not None
                    ):
                        delay_ms = error.retry_after_ms
                    else:
                        delay_ms = backoff_delay_ms(attempt, self._retry)

                    attempt += 1
                    self._fire_hook(
                        "on_retry",
                        {
                            "method": method,
                            "url": url,
                            "attempt": attempt,
                            "delay_ms": delay_ms,
                            "reason": "HTTP {}".format(response.status),
                        },
                    )
                    sleep_ms(int(delay_ms))
                    continue

                raise error

            return response.data

    def get(self, path: str, **options: Any) -> Any:
        return self.request("GET", path, None, **options)

    def post(self, path: str, body: Any = None, **options: Any) -> Any:
        return self.request("POST", path, body, **options)

    def put(self, path: str, body: Any = None, **options: Any) -> Any:
        return self.request("PUT", path, body, **options)

    def patch(self, path: str, body: Any = None, **options: Any) -> Any:
        return self.request("PATCH", path, body, **options)

    def delete(self, path: str, body: Any = None, **options: Any) -> Any:
        return self.request("DELETE", path, body, **options)

    # ------------------------------------------------------------------
    # Internos
    # ------------------------------------------------------------------

    def _build_headers(self, options: Mapping[str, Any]) -> Dict[str, str]:
        headers: Dict[str, str] = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": SDK_USER_AGENT,
        }

        configured = self._config.get("headers")
        if isinstance(configured, Mapping):
            headers.update({str(k): str(v) for k, v in configured.items()})

        bearer_token = options.get("bearer_token") or self.bearer_token
        if bearer_token:
            headers["Authorization"] = "Bearer " + bearer_token

        device_token = options.get("device_token") or self.device_token
        if device_token:
            headers["DeviceToken"] = device_token

        secret_key = options.get("secret_key")
        if secret_key:
            headers["SecretKey"] = str(secret_key)

        extra = options.get("headers")
        if isinstance(extra, Mapping):
            headers.update({str(k): str(v) for k, v in extra.items()})

        return headers

    def _fire_hook(self, name: str, info: Dict[str, Any]) -> None:
        hook = self._hooks.get(name)
        if callable(hook):
            hook(info)


def _encode_body(body: Any) -> str:
    """Serializa o corpo em JSON. Dicionários vazios viram ``{}``."""
    return jsonlib.dumps(body, ensure_ascii=False, separators=(",", ":"))


def _build_query_string(query: Optional[Mapping[str, Any]]) -> str:
    if not query:
        return ""

    parts = []
    for key, value in query.items():
        if value is None:
            continue

        if isinstance(value, bool):
            value = "true" if value else "false"
        elif isinstance(value, (list, tuple)):
            value = ",".join(str(item) for item in value)

        parts.append(quote_plus(str(key)) + "=" + quote_plus(str(value)))

    return "?" + "&".join(parts) if parts else ""


def _join_url(base_url: str, path: str) -> str:
    base = base_url.rstrip("/")
    suffix = str(path).lstrip("/")

    return base if suffix == "" else base + "/" + suffix
