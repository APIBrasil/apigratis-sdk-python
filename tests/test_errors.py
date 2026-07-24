"""Testes da hierarquia de erros e do mapeamento de status HTTP."""

from __future__ import annotations

import pytest

from api_brasil.core.errors import (
    ApiBrasilError,
    AuthenticationError,
    InsufficientBalanceError,
    NotFoundError,
    PermissionError,
    RateLimitError,
    ServerError,
    ValidationError,
    create_api_error,
    parse_retry_after,
)

from .helpers import build_api, http_error


@pytest.mark.parametrize(
    "status,classe",
    [
        (400, ValidationError),
        (422, ValidationError),
        (401, AuthenticationError),
        (402, InsufficientBalanceError),
        (403, PermissionError),
        (404, NotFoundError),
        (410, NotFoundError),
        (429, RateLimitError),
        (500, ServerError),
        (503, ServerError),
    ],
)
def test_mapeia_status_para_subclasse(status, classe):
    erro = create_api_error(status, {"message": "falhou"})

    assert isinstance(erro, classe)
    assert isinstance(erro, ApiBrasilError)
    assert erro.status == status
    assert erro.message == "falhou"


def test_todas_as_subclasses_estendem_apibrasilerror():
    for classe in (
        ValidationError,
        AuthenticationError,
        InsufficientBalanceError,
        PermissionError,
        NotFoundError,
        RateLimitError,
        ServerError,
    ):
        assert issubclass(classe, ApiBrasilError)


def test_extrai_codigo_de_erro():
    erro = create_api_error(404, {"message": "sumiu", "code": "NOT_FOUND"})

    assert erro.code == "NOT_FOUND"


def test_mensagem_padrao_quando_corpo_sem_mensagem():
    erro = create_api_error(500, None)

    assert erro.message == "A API respondeu com HTTP 500."


def test_flags_de_conveniencia():
    assert create_api_error(402, {}).is_insufficient_balance is True
    assert create_api_error(401, {}).is_unauthorized is True
    assert create_api_error(500, {}).is_insufficient_balance is False


def test_rate_limit_retry_after_em_segundos():
    erro = create_api_error(429, {}, {"retry-after": "2"})

    assert isinstance(erro, RateLimitError)
    assert erro.retry_after_ms == 2000


def test_parse_retry_after_invalido():
    assert parse_retry_after(None) is None
    assert parse_retry_after({}) is None
    assert parse_retry_after({"retry-after": "abc"}) is None


def test_http_client_lanca_erro_tipado():
    transport, api = build_api()
    transport.respond_with(http_error(402, {"message": "sem saldo"}))

    with pytest.raises(InsufficientBalanceError) as exc:
        api.consulta.cpf({"cpf": "00000000000"})

    assert exc.value.status == 402
    assert exc.value.response == {"message": "sem saldo"}


def test_erro_preserva_corpo_completo():
    transport, api = build_api()
    transport.respond_with(
        http_error(400, {"message": "inválido", "errors": {"cpf": ["obrigatório"]}})
    )

    with pytest.raises(ValidationError) as exc:
        api.consulta.cpf({})

    assert exc.value.response["errors"] == {"cpf": ["obrigatório"]}


def test_from_exception_repassa_apibrasilerror():
    original = ValidationError("x", status=400)

    assert ApiBrasilError.from_exception(original) is original
