"""Testes da política de retry."""

from __future__ import annotations

import pytest

from api_brasil.core.errors import InsufficientBalanceError, NetworkError, TimeoutError
from api_brasil.core.retry import backoff_delay_ms, resolve_retry

from .helpers import FakeTransport, build_api, http_error, ok


@pytest.fixture(autouse=True)
def _no_sleep(monkeypatch):
    """Não dorme de verdade entre as tentativas."""
    monkeypatch.setattr("api_brasil.core.http.sleep_ms", lambda ms: None)


def test_resolve_retry_padrao():
    resolved = resolve_retry(None)

    assert resolved["retries"] == 2
    assert resolved["retry_on_statuses"] == [429]


def test_resolve_retry_false_desativa():
    assert resolve_retry(False) is None


def test_resolve_retry_merge_parcial():
    resolved = resolve_retry({"retries": 5})

    assert resolved["retries"] == 5
    assert resolved["min_delay_ms"] == 300


def test_backoff_exponencial_respeita_teto():
    retry = {"min_delay_ms": 300, "max_delay_ms": 5000}
    for attempt in range(0, 6):
        assert backoff_delay_ms(attempt, retry) <= 5000


def test_retry_em_429_e_depois_sucesso():
    transport = FakeTransport()
    transport.respond_with(http_error(429, {}), ok({"ok": True}))
    _, api = build_api_com_retry(transport)

    resultado = api.consulta.cpf({"cpf": "0"})

    assert resultado == {"ok": True}
    assert len(transport) == 2


def test_nao_refaz_erro_de_negocio():
    transport = FakeTransport()
    transport.respond_with(http_error(402, {"message": "sem saldo"}))
    _, api = build_api_com_retry(transport)

    with pytest.raises(InsufficientBalanceError):
        api.consulta.cpf({"cpf": "0"})

    assert len(transport) == 1


def test_refaz_falha_de_conexao():
    transport = FakeTransport()
    transport.respond_with(NetworkError("caiu"), ok({"ok": True}))
    _, api = build_api_com_retry(transport)

    assert api.account.balance() == {"ok": True}
    assert len(transport) == 2


def test_nao_refaz_timeout():
    transport = FakeTransport()
    transport.respond_with(TimeoutError("estourou"), ok())
    _, api = build_api_com_retry(transport)

    with pytest.raises(TimeoutError):
        api.account.balance()

    assert len(transport) == 1


def test_respeita_retry_after_do_servidor():
    delays = []
    transport = FakeTransport()
    transport.respond_with(http_error(429, {}, {"retry-after": "3"}), ok())
    _, api = build_api(
        transport=transport,
        retry={"retries": 2},
        hooks={"on_retry": lambda info: delays.append(info["delay_ms"])},
    )

    api.account.balance()

    assert delays == [3000]


def build_api_com_retry(transport):
    return build_api(transport=transport, retry={"retries": 2})
