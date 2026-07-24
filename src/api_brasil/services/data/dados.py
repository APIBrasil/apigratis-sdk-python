"""Dados cadastrais (device-based)."""

from __future__ import annotations

from typing import Any

from ...core.http import HttpClient
from ...core.types import Json
from ..device_proxy import DeviceProxyService

__all__ = ["DadosService"]


class DadosService(DeviceProxyService):
    """Dados cadastrais (device-based): ``/dados/{action}``."""

    def __init__(self, http: HttpClient) -> None:
        super().__init__(http, "dados")

    def cnpj(self, body: Json, **options: Any) -> Any:
        """Consulta CNPJ: ``POST /dados/cnpj`` body ``{"cnpj": ...}``."""
        return self.request("cnpj", body, **options)

    def cpf(self, body: Json, **options: Any) -> Any:
        """Consulta CPF: ``POST /dados/cpf`` body ``{"cpf": ...}``."""
        return self.request("cpf", body, **options)
