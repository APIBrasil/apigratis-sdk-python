"""Testes das camadas de transporte (RequestsTransport e UrllibTransport)."""

from __future__ import annotations

import io

import pytest

from api_brasil.core.errors import NetworkError, TimeoutError
from api_brasil.core.transport import (
    RequestsTransport,
    TransportRequest,
    UrllibTransport,
    default_transport,
)


class FakeResponse:
    def __init__(self, status, content=b"", headers=None):
        self.status_code = status
        self.content = content
        self.headers = headers or {}


class FakeSession:
    def __init__(self, response=None, error=None):
        self._response = response
        self._error = error
        self.calls = []

    def request(self, **kwargs):
        self.calls.append(kwargs)
        if self._error is not None:
            raise self._error
        return self._response


def test_requests_transport_decodifica_json():
    pytest.importorskip("requests")
    session = FakeSession(FakeResponse(200, b'{"ok": true}', {"X-A": "1"}))
    transport = RequestsTransport(session=session)

    response = transport.request(TransportRequest("GET", "https://x/y", {}, None))

    assert response.status == 200
    assert response.data == {"ok": True}
    assert response.headers == {"x-a": "1"}


def test_requests_transport_devolve_status_de_erro_sem_lancar():
    pytest.importorskip("requests")
    session = FakeSession(FakeResponse(404, b'{"message": "sumiu"}'))
    transport = RequestsTransport(session=session)

    response = transport.request(TransportRequest("GET", "https://x/y", {}, None))

    assert response.status == 404
    assert response.data == {"message": "sumiu"}


def test_requests_transport_timeout_vira_timeouterror():
    requests = pytest.importorskip("requests")
    session = FakeSession(error=requests.Timeout("demorou"))
    transport = RequestsTransport(session=session)

    with pytest.raises(TimeoutError):
        transport.request(
            TransportRequest("GET", "https://x/y", {}, None, timeout_ms=100)
        )


def test_requests_transport_falha_de_rede_vira_networkerror():
    requests = pytest.importorskip("requests")
    session = FakeSession(error=requests.ConnectionError("recusou"))
    transport = RequestsTransport(session=session)

    with pytest.raises(NetworkError):
        transport.request(TransportRequest("GET", "https://x/y", {}, None))


def test_requests_transport_raw_devolve_bytes():
    pytest.importorskip("requests")
    session = FakeSession(FakeResponse(200, b"%PDF-1.4"))
    transport = RequestsTransport(session=session)

    response = transport.request(
        TransportRequest("GET", "https://x/y", {}, None, response_type="raw")
    )

    assert response.data == b"%PDF-1.4"


class FakeUrllibResponse(io.BytesIO):
    def __init__(self, status, body, headers):
        super().__init__(body)
        self.status = status
        self.headers = headers

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


class FakeOpener:
    def __init__(self, response):
        self._response = response
        self.calls = []

    def urlopen(self, request, timeout=None):
        self.calls.append((request, timeout))
        return self._response


def test_urllib_transport_decodifica_json():
    opener = FakeOpener(FakeUrllibResponse(200, b'{"ok": true}', {"X-A": "1"}))
    transport = UrllibTransport(opener=opener)

    response = transport.request(TransportRequest("GET", "https://x/y", {}, None))

    assert response.status == 200
    assert response.data == {"ok": True}
    assert response.headers == {"x-a": "1"}


def test_default_transport_retorna_transport():
    from api_brasil.core.transport import Transport

    assert isinstance(default_transport(), Transport)
