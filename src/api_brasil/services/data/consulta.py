"""Consultas por crédito."""

from __future__ import annotations

from typing import Any, Optional

from ...core.http import HttpClient
from ...core.types import Json

__all__ = ["ConsultaService"]


class ConsultaService:
    """Consultas por crédito (``/consulta/{servico}/credits`` e afins).

    Não usam ``DeviceToken`` — debitam o saldo/créditos da conta. O campo
    ``tipo`` do body define o produto consultado (ex: ``serasa-score-pf``,
    ``spc-serasa``) — a lista completa está em
    :data:`api_brasil.generated.catalog.CONSULTA_TIPOS`. Use
    ``homolog=True`` no body para sandbox.
    """

    def __init__(self, http: HttpClient) -> None:
        self.http = http

    def generic(self, service: str, body: Optional[Json] = None, **options: Any) -> Any:
        """Consulta genérica: ``POST /consulta/{service}/credits``."""
        return self.http.post(
            "/consulta/{}/credits".format(service),
            body if body is not None else {},
            **options,
        )

    def cpf(self, body: Json, **options: Any) -> Any:
        """Consulta CPF: ``POST /consulta/cpf/credits``."""
        return self.generic("cpf", body, **options)

    def cnpj(self, body: Json, **options: Any) -> Any:
        """Consulta CNPJ: ``POST /consulta/cnpj/credits``."""
        return self.generic("cnpj", body, **options)

    def cnh(self, body: Json, **options: Any) -> Any:
        """Consulta CNH: ``POST /consulta/cnh/credits``."""
        return self.generic("cnh", body, **options)

    def cep(self, body: Json, **options: Any) -> Any:
        """Consulta CEP: ``POST /consulta/cep/credits``."""
        return self.generic("cep", body, **options)

    def veiculos(self, body: Json, **options: Any) -> Any:
        """Consulta veicular: ``POST /consulta/veiculos/credits``."""
        return self.generic("veiculos", body, **options)

    def telefone(self, body: Json, **options: Any) -> Any:
        """Consulta operadora de telefone: ``POST /consulta/telefone/credits``."""
        return self.generic("telefone", body, **options)

    def veiculos_base(self, base: str, body: Json, **options: Any) -> Any:
        """Consulta veicular nas bases dedicadas.

        ``POST /vehicles/base/000/dados`` | ``POST /vehicles/base/000/fipe``

        :param base: ``dados`` ou ``fipe``
        """
        return self.http.post("/vehicles/base/000/{}".format(base), body, **options)

    def cep_distancia(self, body: Json, **options: Any) -> Any:
        """Distância entre CEPs: ``POST /cep/distancia/calcular``."""
        return self.http.post("/cep/distancia/calcular", body, **options)

    def proxy_seller(self, body: Optional[Json] = None, **options: Any) -> Any:
        """Proxy seller: ``POST /proxy/seller/credits``."""
        return self.http.post(
            "/proxy/seller/credits", body if body is not None else {}, **options
        )
