"""Testes da interface legada (<= 2.0.x) — mantida por compatibilidade."""

from __future__ import annotations

import json
from unittest import mock

import pytest

from api_brasil import (
    APIBrasilClient,
    CEPGeoLocationAPI,
    CNPJApi,
    CPFApi,
    CorreiosAPI,
    SMSApi,
    VehiclesApi,
    WhatsAppApi,
)
from api_brasil.features.vehicles import Endpoints


class FakeHTTPResponse:
    def __init__(self, status_code=200, payload=None, reason="OK"):
        self.status_code = status_code
        self._payload = (
            payload if payload is not None else {"error": False, "response": {}}
        )
        self.reason = reason

    def json(self):
        return self._payload


@pytest.fixture
def client():
    return APIBrasilClient(bearer_token="jwt")


def _patch_post(payload=None, status_code=200):
    return mock.patch(
        "api_brasil.api_client.client_builder.requests.post",
        return_value=FakeHTTPResponse(status_code=status_code, payload=payload),
    )


def test_client_headers(client):
    headers = client._headers(device_token="dev")

    assert headers["Authorization"] == "Bearer jwt"
    assert headers["DeviceToken"] == "dev"
    assert headers["User-Agent"] == "APIBrasil/Python-SDK"


def test_whatsapp_send_message(client):
    whatsapp = WhatsAppApi(api_brasil_client=client, device_token="dev")
    whatsapp.to_number("5511999999999")

    with _patch_post({"error": False, "response": "ok"}) as post:
        response, status = whatsapp.send_message("Olá!")

    assert status == 200
    args, kwargs = post.call_args
    assert kwargs["url"].endswith("/whatsapp/sendText")
    assert json.loads(kwargs["data"])["number"] == "5511999999999"


def test_whatsapp_sem_numero_falha(client):
    whatsapp = WhatsAppApi(api_brasil_client=client, device_token="dev")

    with pytest.raises(ValueError):
        whatsapp.send_message("Olá!")


def test_cnpj_consulta(client):
    cnpj = CNPJApi(api_brasil_client=client, device_token="dev")
    cnpj.set_cnpj("44.959.669/0001-80")

    with _patch_post() as post:
        cnpj.consulta()

    assert post.call_args.kwargs["url"].endswith("/dados/cnpj")


def test_cpf_consulta(client):
    cpf = CPFApi(api_brasil_client=client, device_token="dev")
    cpf.set_cpf("00000000000")

    with _patch_post() as post:
        cpf.consulta()

    assert post.call_args.kwargs["url"].endswith("/dados/cpf")


def test_cep_consulta(client):
    cep = CEPGeoLocationAPI(api_brasil_client=client, device_token="dev")
    cep.set_cep("00000-000")

    with _patch_post() as post:
        cep.consulta()

    assert post.call_args.kwargs["url"].endswith("/cep/cep")


def test_correios_track(client):
    correios = CorreiosAPI(api_brasil_client=client, device_token="dev")
    correios.set_track_code("PN123456789BR")

    with _patch_post() as post:
        correios.track()

    assert post.call_args.kwargs["url"].endswith("/correios/rastreio")


def test_sms_send(client):
    sms = SMSApi(api_brasil_client=client, device_token="dev")
    sms.set_phone_number("5511999999999")

    with _patch_post() as post:
        sms.send("Olá!")

    assert post.call_args.kwargs["url"].endswith("/sms/send")


def test_vehicles_consulta(client):
    vehicles = VehiclesApi(api_brasil_client=client, device_token="dev")
    vehicles.set_plate("ABC-1234")

    with _patch_post() as post:
        vehicles.consulta(vechiles_api_endpoint=Endpoints.dados)

    assert post.call_args.kwargs["url"].endswith("/vehicles/dados")
