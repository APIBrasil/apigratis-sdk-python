"""Testes do cliente ApiBrasil: wiring dos serviços, credenciais e porta genérica."""

from __future__ import annotations

import pytest

from api_brasil import ApiBrasil, ApiBrasilError
from api_brasil.core.http import DEFAULT_BASE_URL, DEFAULT_TIMEOUT, SDK_USER_AGENT
from api_brasil.services.device_proxy import DeviceProxyService

from .helpers import BASE, FakeTransport, build_api, ok

SERVICOS = [
    "auth",
    "devices",
    "whatsapp",
    "evolution",
    "whatsmeow",
    "sms",
    "dados",
    "vehicles",
    "fipe",
    "correios",
    "cep",
    "geolocation",
    "geomatrix",
    "recognize",
    "ddd",
    "holidays",
    "translate",
    "weather",
    "loterias",
    "database_ip",
    "consulta",
    "ura",
    "chip_virtual",
    "bulk",
    "catalog",
    "account",
    "payments",
    "ip_whitelist",
    "bearer_rate_limit",
    "reports",
]


@pytest.mark.parametrize("nome", SERVICOS)
def test_expoe_todos_os_servicos(nome):
    _, api = build_api()

    assert getattr(api, nome) is not None


@pytest.mark.parametrize("nome", SERVICOS)
def test_todos_os_servicos_compartilham_o_mesmo_http(nome):
    _, api = build_api()

    assert getattr(api, nome).http is api.http


def test_defaults_do_cliente():
    api = ApiBrasil(transport=FakeTransport())

    assert api.http.base_url == DEFAULT_BASE_URL
    assert DEFAULT_TIMEOUT == 30000
    assert SDK_USER_AGENT == "APIBRASIL/SDK-PYTHON"


def test_le_credenciais_do_ambiente(monkeypatch):
    monkeypatch.setenv("APIBRASIL_BEARER_TOKEN", "jwt-env")
    monkeypatch.setenv("APIBRASIL_DEVICE_TOKEN", "dev-env")
    monkeypatch.setenv("APIBRASIL_SECRET_KEY", "secret-env")
    monkeypatch.setenv("APIBRASIL_BASE_URL", "https://homolog.local/api/v2")

    api = ApiBrasil(transport=FakeTransport())

    assert api.http.bearer_token == "jwt-env"
    assert api.http.device_token == "dev-env"
    assert api.http.secret_key == "secret-env"
    assert api.http.base_url == "https://homolog.local/api/v2"


def test_config_explicita_tem_prioridade_sobre_ambiente(monkeypatch):
    monkeypatch.setenv("APIBRASIL_BEARER_TOKEN", "jwt-env")

    api = ApiBrasil(transport=FakeTransport(), bearer_token="jwt-explicito")

    assert api.http.bearer_token == "jwt-explicito"


def test_aceita_config_como_dicionario():
    transport = FakeTransport()
    api = ApiBrasil({"transport": transport, "bearer_token": "jwt", "retry": False})

    assert api.http.bearer_token == "jwt"
    assert api.http.transport is transport


def test_config_desconhecida_falha():
    with pytest.raises(TypeError, match="Configuração desconhecida"):
        ApiBrasil(bearerToken="jwt")


def test_set_bearer_token_e_encadeavel():
    transport, api = build_api()

    assert api.set_bearer_token("novo") is api

    api.account.balance()

    assert transport.last_headers["Authorization"] == "Bearer novo"


def test_set_device_token_e_encadeavel():
    transport, api = build_api()

    assert api.set_device_token("novo-device") is api

    api.whatsapp.send_text({"number": "5511999999999", "text": "oi"})

    assert transport.last_headers["DeviceToken"] == "novo-device"


def test_with_device_cria_novo_cliente_com_mesmas_credenciais():
    transport, api = build_api()
    outro = api.with_device("device-2")

    assert outro is not api
    assert outro.http.device_token == "device-2"
    assert outro.http.bearer_token == api.http.bearer_token
    # o transporte é reaproveitado
    assert outro.http.transport is transport

    outro.whatsapp.send_text({"number": "55", "text": "oi"})

    assert transport.last_headers["DeviceToken"] == "device-2"
    assert api.http.device_token == "dev"


def test_request_generico():
    transport, api = build_api()
    api.request("POST", "/consulta/cpf/credits", {"cpf": "00000000000"})

    assert transport.last.method == "POST"
    assert transport.last.url == BASE + "/consulta/cpf/credits"
    assert transport.last_body == {"cpf": "00000000000"}


def test_request_generico_get_sem_body():
    transport, api = build_api()
    api.request("GET", "/reports/quick-stats")

    assert transport.last.method == "GET"
    assert transport.last.url == BASE + "/reports/quick-stats"
    assert transport.last.body is None


def test_login_retorna_cliente_autenticado():
    transport = FakeTransport()
    transport.respond_with(ok({"authorization": {"token": "jwt-do-login"}}))

    client, session = ApiBrasil.login(
        {"email": "voce@empresa.com.br", "password": "******"},
        transport=transport,
        retry=False,
        base_url=BASE,
    )

    assert isinstance(client, ApiBrasil)
    assert client.http.bearer_token == "jwt-do-login"
    assert session["authorization"]["token"] == "jwt-do-login"
    assert transport.last.url == BASE + "/auth/login"


def test_login_com_2fa_lanca_erro():
    transport = FakeTransport()
    transport.respond_with(ok({"requires_2fa": True, "challenge": "abc"}))

    with pytest.raises(ApiBrasilError, match="dois fatores"):
        ApiBrasil.login(
            {"email": "voce@empresa.com.br", "password": "******"},
            transport=transport,
            retry=False,
            base_url=BASE,
        )


@pytest.mark.parametrize(
    "atributo,servico",
    [
        ("geolocation", "geolocation"),
        ("geomatrix", "geomatrix"),
        ("recognize", "recognize"),
        ("ddd", "ddd"),
        ("holidays", "holidays"),
        ("translate", "translate"),
        ("weather", "weather"),
        ("loterias", "loterias"),
    ],
)
def test_servicos_device_proxy(atributo, servico):
    transport, api = build_api()
    proxy = getattr(api, atributo)

    assert isinstance(proxy, DeviceProxyService)
    assert proxy.service == servico

    proxy.request("acao", {"campo": 1})

    assert transport.last.url == BASE + "/{}/acao".format(servico)
    assert transport.last_body == {"campo": 1}
