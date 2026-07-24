"""Veículos por placa (device-based)."""

from __future__ import annotations

from typing import Any
from urllib.parse import quote

from ...core.http import HttpClient
from ...core.types import Json
from ..device_proxy import DeviceProxyService

__all__ = ["VehiclesService"]


class VehiclesService(DeviceProxyService):
    """Veículos por placa (device-based): ``/vehicles/{action}``."""

    def __init__(self, http: HttpClient) -> None:
        super().__init__(http, "vehicles")

    def dados(self, body: Json, **options: Any) -> Any:
        """Dados do veículo pela placa: ``POST /vehicles/dados`` body ``{"placa": ...}``."""
        return self.request("dados", body, **options)

    def fipe(self, body: Json, **options: Any) -> Any:
        """FIPE pela placa: ``POST /vehicles/fipe`` body ``{"placa": ...}``."""
        return self.request("fipe", body, **options)

    def consulta_fipe(self, placa: str, **options: Any) -> Any:
        """Consulta FIPE: ``POST /vehicles/consultafipe/{placa}``."""
        return self.request("consultafipe/" + quote(placa, safe=""), None, **options)
