"""Camada de transporte HTTP da SDK.

A implementação padrão usa ``requests`` (:class:`RequestsTransport`), com
fallback para a stdlib (:class:`UrllibTransport`); injete a sua para usar
proxies, outro cliente HTTP, mocks de teste etc.

Contrato: retorna a resposta para QUALQUER status HTTP; lança
:class:`~api_brasil.core.errors.NetworkError` /
:class:`~api_brasil.core.errors.TimeoutError` apenas quando não houve resposta.
"""

from __future__ import annotations

import json as jsonlib
import socket
import urllib.error
import urllib.request
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from .errors import NetworkError, TimeoutError

__all__ = [
    "TransportRequest",
    "TransportResponse",
    "Transport",
    "RequestsTransport",
    "UrllibTransport",
    "default_transport",
]

_RAW_TYPES = ("raw", "bytes", "arraybuffer")


@dataclass
class TransportRequest:
    """Requisição entregue à camada de transporte.

    Já com URL absoluta, headers montados e corpo serializado.
    """

    method: str
    url: str
    headers: Dict[str, str] = field(default_factory=dict)
    #: Corpo já serializado (JSON).
    body: Optional[str] = None
    #: Timeout em milissegundos.
    timeout_ms: Optional[int] = None
    #: ``json`` (padrão), ``raw``/``bytes`` (binário), ``text`` ou ``stream``.
    response_type: Optional[str] = None


@dataclass
class TransportResponse:
    """Resposta devolvida pela camada de transporte."""

    status: int
    #: Headers com nomes em minúsculas.
    headers: Dict[str, str] = field(default_factory=dict)
    #: Corpo já decodificado (JSON → dict; texto; binário; stream).
    data: Any = None


class Transport(ABC):
    """Interface do transporte HTTP."""

    @abstractmethod
    def request(self, request: TransportRequest) -> TransportResponse:
        """Executa a requisição e devolve a resposta bruta."""


def _decode_body(request: TransportRequest, raw: bytes) -> Any:
    if request.response_type in _RAW_TYPES:
        return raw

    text = raw.decode("utf-8", errors="replace")

    if request.response_type == "text":
        return text

    if text == "":
        return None

    try:
        return jsonlib.loads(text)
    except ValueError:
        return text


def _timeout_seconds(request: TransportRequest) -> Optional[float]:
    if request.timeout_ms is None or request.timeout_ms <= 0:
        return None

    return request.timeout_ms / 1000


class RequestsTransport(Transport):
    """Transporte padrão, baseado na biblioteca ``requests``.

    ``session`` permite reaproveitar conexões (keep-alive) e ``options``
    aceita qualquer argumento de ``Session.request`` (``proxies``, ``verify``,
    ``cert``...).
    """

    def __init__(self, session: Any = None, **options: Any) -> None:
        try:
            import requests  # noqa: F401
        except ImportError as error:  # pragma: no cover - ambiente sem requests
            raise NetworkError(
                "A biblioteca 'requests' não está instalada. "
                "Instale-a ou use UrllibTransport."
            ) from error

        self.session = session
        self.options = options

    def request(self, request: TransportRequest) -> TransportResponse:
        import requests

        session = self.session or requests
        stream = request.response_type == "stream"

        try:
            response = session.request(
                method=request.method,
                url=request.url,
                headers=request.headers,
                data=request.body.encode("utf-8") if request.body is not None else None,
                timeout=_timeout_seconds(request),
                allow_redirects=True,
                stream=stream,
                **self.options,
            )
        except requests.Timeout as error:
            raise TimeoutError(
                "Tempo limite de {}ms excedido em {} {}.".format(
                    request.timeout_ms or 0, request.method, request.url
                ),
                cause=error,
            ) from error
        except requests.RequestException as error:
            raise NetworkError(
                "Falha de rede em {} {}: {}".format(request.method, request.url, error),
                cause=error,
            ) from error

        headers = {
            str(name).lower(): str(value) for name, value in response.headers.items()
        }

        if stream:
            return TransportResponse(response.status_code, headers, response.raw)

        return TransportResponse(
            response.status_code, headers, _decode_body(request, response.content)
        )


class UrllibTransport(Transport):
    """Transporte sem dependências, usando apenas a stdlib.

    Usado automaticamente quando ``requests`` não está instalado.
    """

    def __init__(self, opener: Any = None) -> None:
        self.opener = opener

    def request(self, request: TransportRequest) -> TransportResponse:
        payload = request.body.encode("utf-8") if request.body is not None else None
        http_request = urllib.request.Request(
            request.url,
            data=payload,
            headers=request.headers,
            method=request.method,
        )

        opener = self.opener or urllib.request
        timeout = _timeout_seconds(request)

        try:
            if timeout is None:
                response = opener.urlopen(http_request)
            else:
                response = opener.urlopen(http_request, timeout=timeout)
        except urllib.error.HTTPError as error:
            # HTTPError é uma resposta HTTP completa — não é falha de rede.
            response = error
        except socket.timeout as error:
            raise TimeoutError(
                "Tempo limite de {}ms excedido em {} {}.".format(
                    request.timeout_ms or 0, request.method, request.url
                ),
                cause=error,
            ) from error
        except urllib.error.URLError as error:
            if isinstance(error.reason, socket.timeout):
                raise TimeoutError(
                    "Tempo limite de {}ms excedido em {} {}.".format(
                        request.timeout_ms or 0, request.method, request.url
                    ),
                    cause=error,
                ) from error

            raise NetworkError(
                "Falha de rede em {} {}: {}".format(
                    request.method, request.url, error.reason
                ),
                cause=error,
            ) from error
        except OSError as error:
            raise NetworkError(
                "Falha de rede em {} {}: {}".format(request.method, request.url, error),
                cause=error,
            ) from error

        headers = {
            str(name).lower(): str(value) for name, value in response.headers.items()
        }
        status = int(response.status if response.status is not None else 0)

        if request.response_type == "stream":
            return TransportResponse(status, headers, response)

        with response:
            raw = response.read()

        return TransportResponse(status, headers, _decode_body(request, raw))


def default_transport() -> Transport:
    """``RequestsTransport`` quando ``requests`` está disponível, senão stdlib."""
    try:
        import requests  # noqa: F401
    except ImportError:  # pragma: no cover - ambiente sem requests
        return UrllibTransport()

    return RequestsTransport()
