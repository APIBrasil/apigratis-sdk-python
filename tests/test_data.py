"""Testes de rota dos serviços de dados e consultas."""

from __future__ import annotations

import pytest

from api_brasil import ApiBrasil

from .helpers import assert_route

CASOS = [
    # Dados
    (lambda api: api.dados.cnpj({"cnpj": "0"}), "/dados/cnpj", "POST", {"cnpj": "0"}),
    (lambda api: api.dados.cpf({"cpf": "0"}), "/dados/cpf", "POST", {"cpf": "0"}),
    (
        lambda api: api.dados.request("telefone", {"t": "1"}),
        "/dados/telefone",
        "POST",
        None,
    ),
    # Vehicles
    (
        lambda api: api.vehicles.dados({"placa": "ABC1234"}),
        "/vehicles/dados",
        "POST",
        {"placa": "ABC1234"},
    ),
    (
        lambda api: api.vehicles.fipe({"placa": "ABC1234"}),
        "/vehicles/fipe",
        "POST",
        {"placa": "ABC1234"},
    ),
    (
        lambda api: api.vehicles.consulta_fipe("ABC1234"),
        "/vehicles/consultafipe/ABC1234",
        "POST",
        None,
    ),
    # FIPE
    (
        lambda api: api.fipe.request("ConsultarMarcas", {"x": 1}),
        "/fipe/ConsultarMarcas",
        "POST",
        None,
    ),
    # Correios / CEP
    (
        lambda api: api.correios.rastreio({"code": "NL"}),
        "/correios/rastreio",
        "POST",
        {"code": "NL"},
    ),
    (lambda api: api.cep.cep({"cep": "0"}), "/cep/cep", "POST", {"cep": "0"}),
    # Consulta por crédito
    (
        lambda api: api.consulta.cpf({"cpf": "0"}),
        "/consulta/cpf/credits",
        "POST",
        {"cpf": "0"},
    ),
    (
        lambda api: api.consulta.cnpj({"cnpj": "0"}),
        "/consulta/cnpj/credits",
        "POST",
        {"cnpj": "0"},
    ),
    (lambda api: api.consulta.cnh({"cpf": "0"}), "/consulta/cnh/credits", "POST", None),
    (lambda api: api.consulta.cep({"cep": "0"}), "/consulta/cep/credits", "POST", None),
    (
        lambda api: api.consulta.veiculos({"placa": "A"}),
        "/consulta/veiculos/credits",
        "POST",
        None,
    ),
    (
        lambda api: api.consulta.telefone({"numbers": []}),
        "/consulta/telefone/credits",
        "POST",
        None,
    ),
    (
        lambda api: api.consulta.generic(
            "cpf", {"cpf": "0", "tipo": "serasa-score-pf"}
        ),
        "/consulta/cpf/credits",
        "POST",
        {"cpf": "0", "tipo": "serasa-score-pf"},
    ),
    (
        lambda api: api.consulta.veiculos_base("dados", {"placa": "A"}),
        "/vehicles/base/000/dados",
        "POST",
        None,
    ),
    (
        lambda api: api.consulta.cep_distancia({"de": "A", "para": "B"}),
        "/cep/distancia/calcular",
        "POST",
        None,
    ),
    (lambda api: api.consulta.proxy_seller(), "/proxy/seller/credits", "POST", {}),
    # URA / Chip / Bulk / DatabaseIp
    (lambda api: api.ura.dialler({"x": 1}), "/ura/call/dialler", "POST", None),
    (lambda api: api.ura.status({"x": 1}), "/ura/call/status", "POST", None),
    (lambda api: api.chip_virtual.operators(), "/chip/virtual/operators", "POST", None),
    (lambda api: api.chip_virtual.buy({"x": 1}), "/chip/virtual/buy", "POST", None),
    (
        lambda api: api.chip_virtual.activation({"x": 1}),
        "/chip/virtual/activation",
        "POST",
        None,
    ),
    (lambda api: api.chip_virtual.services(), "/chip/virtual/services", "POST", None),
    (lambda api: api.bulk.direct("cpf", {"x": 1}), "/bulk/direct/cpf", "POST", None),
    (lambda api: api.bulk.queue("cpf", {"x": 1}), "/bulk/queue/cpf", "POST", None),
    (
        lambda api: api.database_ip.ip({"ip": "1.1.1.1"}),
        "/database/ip",
        "POST",
        {"ip": "1.1.1.1"},
    ),
]


@pytest.mark.parametrize("call,path,method,body", CASOS)
def test_rota(call, path, method, body):
    assert_route(call, path, method, body)
