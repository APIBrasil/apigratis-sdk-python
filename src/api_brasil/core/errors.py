"""Hierarquia de erros da SDK.

Todo erro lançado pelo cliente :class:`~api_brasil.client.ApiBrasil` estende
:class:`ApiBrasilError`, o que permite tratar cada categoria separadamente:

- :class:`ValidationError` (400/422), :class:`AuthenticationError` (401),
  :class:`InsufficientBalanceError` (402), :class:`PermissionError` (403),
  :class:`NotFoundError` (404/410), :class:`RateLimitError` (429),
  :class:`ServerError` (5xx)
- :class:`NetworkError` / :class:`TimeoutError` para falhas antes da resposta.

.. note::
   ``PermissionError`` e ``TimeoutError`` têm o mesmo nome de builtins do
   Python (paridade com as SDKs Node/PHP/Flutter). Os aliases
   :class:`ApiBrasilPermissionError` e :class:`ApiBrasilTimeoutError` evitam
   o sombreamento quando você importa os erros no escopo do seu módulo.
"""

from __future__ import annotations

import email.utils
import time
from typing import Any, Mapping, Optional

__all__ = [
    "ApiBrasilError",
    "NetworkError",
    "TimeoutError",
    "ValidationError",
    "AuthenticationError",
    "InsufficientBalanceError",
    "PermissionError",
    "NotFoundError",
    "RateLimitError",
    "ServerError",
    "ApiBrasilPermissionError",
    "ApiBrasilTimeoutError",
    "create_api_error",
]


class ApiBrasilError(Exception):
    """Erro base lançado pelo cliente ``ApiBrasil``."""

    def __init__(
        self,
        message: str,
        *,
        status: Optional[int] = None,
        code: Optional[str] = None,
        response: Any = None,
        cause: Optional[BaseException] = None,
    ) -> None:
        super().__init__(message)

        #: Mensagem de erro (da API quando disponível).
        self.message = message
        #: Status HTTP retornado pela API (ex: 401, 402, 404).
        self.status = status
        #: Código de erro retornado pela API (ex: ``NOT_FOUND``).
        self.code = code
        #: Corpo completo da resposta de erro, quando existir.
        self.response = response

        if cause is not None:
            self.__cause__ = cause

    @property
    def is_insufficient_balance(self) -> bool:
        """``True`` quando a falha foi por saldo/créditos insuficientes (HTTP 402)."""
        return self.status == 402

    @property
    def is_unauthorized(self) -> bool:
        """``True`` quando a falha foi de autenticação (HTTP 401)."""
        return self.status == 401

    @classmethod
    def from_exception(cls, error: Any) -> "ApiBrasilError":
        """Converte qualquer erro em um ``ApiBrasilError``.

        Preserva status e corpo quando a exceção original carrega uma
        resposta HTTP (``requests.RequestException``).
        """
        if isinstance(error, ApiBrasilError):
            return error

        response = getattr(error, "response", None)
        status = getattr(response, "status_code", None)
        if response is not None and isinstance(status, int):
            try:
                data: Any = response.json()
            except Exception:  # noqa: BLE001 - corpo não-JSON
                data = getattr(response, "text", None)

            headers = {
                str(name).lower(): str(value)
                for name, value in dict(getattr(response, "headers", {}) or {}).items()
            }

            return create_api_error(status, data, headers, cause=error)

        if isinstance(error, BaseException):
            return ApiBrasilError(str(error) or error.__class__.__name__, cause=error)

        return ApiBrasilError(str(error) if error is not None else "Erro desconhecido.")

    def __repr__(self) -> str:  # pragma: no cover - conveniência no REPL
        return "{}({!r}, status={!r}, code={!r})".format(
            self.__class__.__name__, self.message, self.status, self.code
        )


class NetworkError(ApiBrasilError):
    """Falha de conexão — a requisição não chegou a receber resposta."""


class TimeoutError(NetworkError):  # noqa: A001 - paridade com as demais SDKs
    """Tempo limite da requisição excedido."""


class ValidationError(ApiBrasilError):
    """HTTP 400/422 — payload inválido."""


class AuthenticationError(ApiBrasilError):
    """HTTP 401 — Bearer Token ausente, inválido ou expirado."""


class InsufficientBalanceError(ApiBrasilError):
    """HTTP 402 — saldo/créditos insuficientes."""


class PermissionError(ApiBrasilError):  # noqa: A001 - paridade com as demais SDKs
    """HTTP 403 — sem permissão para o recurso."""


class NotFoundError(ApiBrasilError):
    """HTTP 404/410 — recurso não encontrado ou rota desativada."""


class RateLimitError(ApiBrasilError):
    """HTTP 429 — rate limit atingido."""

    def __init__(
        self, message: str, *, retry_after_ms: Optional[int] = None, **kwargs: Any
    ) -> None:
        super().__init__(message, **kwargs)

        #: Espera sugerida pelo servidor (header ``Retry-After``), em ms.
        self.retry_after_ms = retry_after_ms


class ServerError(ApiBrasilError):
    """HTTP 5xx — erro do gateway ou do provedor."""


#: Alias de :class:`PermissionError` que não sombreia o builtin do Python.
ApiBrasilPermissionError = PermissionError

#: Alias de :class:`TimeoutError` que não sombreia o builtin do Python.
ApiBrasilTimeoutError = TimeoutError


def create_api_error(
    status: int,
    data: Any = None,
    headers: Optional[Mapping[str, str]] = None,
    *,
    cause: Optional[BaseException] = None,
) -> ApiBrasilError:
    """Mapeia status HTTP + corpo de erro para a subclasse adequada."""
    message = _extract_message(status, data)
    kwargs = {
        "status": status,
        "code": _extract_code(data),
        "response": data,
        "cause": cause,
    }

    if status in (400, 422):
        return ValidationError(message, **kwargs)

    if status == 401:
        return AuthenticationError(message, **kwargs)

    if status == 402:
        return InsufficientBalanceError(message, **kwargs)

    if status == 403:
        return PermissionError(message, **kwargs)

    if status in (404, 410):
        return NotFoundError(message, **kwargs)

    if status == 429:
        return RateLimitError(
            message, retry_after_ms=parse_retry_after(headers), **kwargs
        )

    if status >= 500:
        return ServerError(message, **kwargs)

    return ApiBrasilError(message, **kwargs)


def _extract_message(status: int, data: Any) -> str:
    if isinstance(data, Mapping):
        for key in ("message", "error"):
            value = data.get(key)
            if isinstance(value, str) and value:
                return value

    return "A API respondeu com HTTP {}.".format(status)


def _extract_code(data: Any) -> Optional[str]:
    if isinstance(data, Mapping):
        code = data.get("code")
        if isinstance(code, str):
            return code

    return None


def parse_retry_after(headers: Optional[Mapping[str, str]]) -> Optional[int]:
    """Lê o header ``Retry-After`` (segundos ou data HTTP) e devolve ms."""
    if not headers:
        return None

    raw = headers.get("retry-after") or headers.get("Retry-After")
    if raw is None or raw == "":
        return None

    try:
        return max(0, int(float(raw) * 1000))
    except (TypeError, ValueError):
        pass

    try:
        at = email.utils.parsedate_to_datetime(str(raw))
    except (TypeError, ValueError):
        return None

    if at is None:
        return None

    return max(0, int((at.timestamp() - time.time()) * 1000))
