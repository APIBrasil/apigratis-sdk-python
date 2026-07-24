"""Helpers dos testes: transporte fake e montagem do cliente."""

from __future__ import annotations

import json
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from api_brasil import ApiBrasil
from api_brasil.core.transport import Transport, TransportRequest, TransportResponse

BASE = "https://gateway.apibrasil.io/api/v2"


def ok(data: Any = None) -> TransportResponse:
    """Resposta 200 com corpo JSON."""
    return TransportResponse(200, {}, {"ok": True} if data is None else data)


def http_error(
    status: int, data: Any = None, headers: Optional[Dict[str, str]] = None
) -> TransportResponse:
    """Resposta de erro HTTP."""
    return TransportResponse(status, headers or {}, data)


class FakeTransport(Transport):
    """Transporte fake: grava todas as requisições e responde com uma fila
    programável (ou um fallback 200)."""

    def __init__(self) -> None:
        self.calls: List[TransportRequest] = []
        self._queue: List[Union[TransportResponse, BaseException]] = []
        self.fallback: TransportResponse = ok()

    def respond_with(
        self, *responses: Union[TransportResponse, BaseException]
    ) -> "FakeTransport":
        """Enfileira respostas (ou erros a lançar), consumidas em ordem."""
        self._queue.extend(responses)

        return self

    def set_fallback(self, response: TransportResponse) -> "FakeTransport":
        """Define a resposta padrão quando a fila está vazia."""
        self.fallback = response

        return self

    @property
    def last(self) -> TransportRequest:
        if not self.calls:
            raise AssertionError("Nenhuma requisição foi feita.")

        return self.calls[-1]

    @property
    def last_body(self) -> Optional[Any]:
        body = self.last.body

        return None if body is None else json.loads(body)

    @property
    def last_headers(self) -> Dict[str, str]:
        return self.last.headers

    def __len__(self) -> int:
        return len(self.calls)

    def request(self, request: TransportRequest) -> TransportResponse:
        self.calls.append(request)
        nxt = self._queue.pop(0) if self._queue else self.fallback

        if isinstance(nxt, BaseException):
            raise nxt

        return nxt


def build_api(**config: Any) -> Tuple[FakeTransport, ApiBrasil]:
    """Cliente ``ApiBrasil`` com transporte fake, retry desligado e credenciais fixas."""
    transport = FakeTransport()
    defaults: Dict[str, Any] = {
        "transport": transport,
        "retry": False,
        "base_url": BASE,
        "bearer_token": "jwt",
        "device_token": "dev",
    }
    defaults.update(config)

    return transport, ApiBrasil(**defaults)


def assert_route(
    call: Callable[[ApiBrasil], Any],
    path: str,
    method: str = "POST",
    body: Any = None,
) -> None:
    """Executa uma chamada da SDK e confere a requisição resultante."""
    transport, api = build_api()
    call(api)

    assert transport.last.method == method
    assert transport.last.url == BASE + path

    if body is not None:
        assert transport.last_body == body
