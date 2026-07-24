"""Testes do núcleo HTTP: headers, URL, query, body, opções e hooks."""

from __future__ import annotations

import json

import pytest

from api_brasil.core.http import HttpClient
from api_brasil.core.transport import TransportResponse

from .helpers import BASE, FakeTransport, build_api, http_error, ok


def build_http(**config):
    transport = FakeTransport()
    config.setdefault("retry", False)
    config.setdefault("base_url", BASE)
    return transport, HttpClient(transport=transport, **config)


def test_injeta_headers_de_autenticacao():
    transport, http = build_http(bearer_token="jwt", device_token="dev")
    http.get("/balance")

    headers = transport.last_headers
    assert headers["Authorization"] == "Bearer jwt"
    assert headers["DeviceToken"] == "dev"
    assert headers["Content-Type"] == "application/json"
    assert headers["Accept"] == "application/json"
    assert headers["User-Agent"] == "APIBRASIL/SDK-PYTHON"


def test_secret_key_apenas_quando_informada():
    transport, http = build_http(bearer_token="jwt")
    http.post("/devices/store", {"x": 1}, secret_key="segredo")

    assert transport.last_headers["SecretKey"] == "segredo"

    http.get("/balance")
    assert "SecretKey" not in transport.last_headers


def test_headers_extras_por_config_e_por_request():
    transport, http = build_http(headers={"X-Global": "g"})
    http.get("/status", headers={"X-Req": "r"})

    assert transport.last_headers["X-Global"] == "g"
    assert transport.last_headers["X-Req"] == "r"


def test_opcoes_por_request_sobrescrevem_config():
    transport, http = build_http(bearer_token="jwt", device_token="dev")
    http.get("/balance", bearer_token="outro", device_token="outro-dev")

    assert transport.last_headers["Authorization"] == "Bearer outro"
    assert transport.last_headers["DeviceToken"] == "outro-dev"


def test_monta_url_juntando_base_e_path():
    transport, http = build_http()
    http.get("/devices")

    assert transport.last.url == BASE + "/devices"


def test_query_string():
    transport, http = build_http()
    http.get("/devices", query={"paginate": True, "page": 2, "vazio": None})

    assert transport.last.url == BASE + "/devices?paginate=true&page=2"


def test_query_string_com_lista():
    transport, http = build_http()
    http.get("/x", query={"ids": [1, 2, 3]})

    assert transport.last.url == BASE + "/x?ids=1%2C2%2C3"


def test_body_serializado_em_json():
    transport, http = build_http()
    http.post("/x", {"a": 1, "b": "dois"})

    assert json.loads(transport.last.body) == {"a": 1, "b": "dois"}


def test_body_none_nao_serializa():
    transport, http = build_http()
    http.post("/x", None)

    assert transport.last.body is None


def test_body_dict_vazio_vira_objeto_json():
    transport, http = build_http()
    http.post("/x", {})

    assert transport.last.body == "{}"


def test_retorna_corpo_decodificado():
    transport, http = build_http()
    transport.respond_with(ok({"saldo": 10}))

    assert http.post("/x") == {"saldo": 10}


def test_verbos_http():
    transport, http = build_http()
    for verbo, metodo in [
        ("GET", http.get),
        ("POST", http.post),
        ("PUT", http.put),
        ("PATCH", http.patch),
        ("DELETE", http.delete),
    ]:
        metodo("/x")
        assert transport.last.method == verbo


def test_opcao_desconhecida_falha():
    _, http = build_http()

    with pytest.raises(TypeError, match="Opção de requisição desconhecida"):
        http.get("/x", deviceToken="dev")


def test_hooks_de_observabilidade():
    eventos = []
    transport, http = build_http(
        hooks={
            "on_request": lambda info: eventos.append(("request", info["attempt"])),
            "on_response": lambda info: eventos.append(("response", info["status"])),
        }
    )
    transport.respond_with(ok())
    http.get("/x")

    assert ("request", 0) in eventos
    assert ("response", 200) in eventos


def test_response_type_raw_devolve_bytes():
    transport, http = build_http()
    transport.respond_with(TransportResponse(200, {}, b"%PDF-1.4"))

    resultado = http.get("/x", response_type="raw")

    assert resultado == b"%PDF-1.4"
    assert transport.last.response_type == "raw"


def test_set_e_get_bearer_token():
    _, http = build_http(bearer_token="jwt")

    assert http.bearer_token == "jwt"
    http.set_bearer_token("novo")
    assert http.bearer_token == "novo"
    http.set_bearer_token(None)
    assert http.bearer_token is None


def test_get_config_inclui_transporte():
    transport, http = build_http(bearer_token="jwt")
    config = http.get_config()

    assert config["bearer_token"] == "jwt"
    assert config["transport"] is transport
