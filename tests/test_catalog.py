"""Testes do catálogo gerado."""

from __future__ import annotations

from api_brasil.generated import catalog


def test_contagens_do_catalogo():
    assert len(catalog.WHATSAPP_ACTIONS) == 121
    assert len(catalog.EVOLUTION_PATHS) == 49
    assert len(catalog.WHATSMEOW_ACTIONS) == 36
    assert len(catalog.CONSULTA_SERVICOS) == 16
    assert len(catalog.CONSULTA_TIPOS) == 210
    assert len(catalog.SERVICE_ACTIONS) == 38


def test_actions_conhecidas():
    assert "sendText" in catalog.WHATSAPP_ACTIONS
    assert "sendFile" in catalog.WHATSAPP_ACTIONS
    assert "message/sendText" in catalog.EVOLUTION_PATHS
    assert "send/text" in catalog.WHATSMEOW_ACTIONS


def test_consulta_tipo():
    assert catalog.consulta_tipo("serasa-score-pf") == {
        "service": "cpf",
        "fields": ["cpf"],
    }
    assert catalog.consulta_tipo("nao-existe") is None


def test_service_actions():
    whatsmeow = catalog.service_actions("whatsmeow")
    assert "send/text" in whatsmeow
    assert catalog.service_actions("inexistente") == []


def test_consulta_servicos_ordenados():
    assert catalog.CONSULTA_SERVICOS == sorted(catalog.CONSULTA_SERVICOS)
