"""Correios (device-based)."""

from __future__ import annotations

from typing import Any

from ...core.http import HttpClient
from ...core.types import Json
from ..device_proxy import DeviceProxyService

__all__ = ["CorreiosService"]


class CorreiosService(DeviceProxyService):
    """Correios (device-based): ``/correios/{action}``."""

    def __init__(self, http: HttpClient) -> None:
        super().__init__(http, "correios")

    def rastreio(self, body: Json, **options: Any) -> Any:
        """Rastreio de encomendas: ``POST /correios/rastreio`` body ``{"code": ...}``."""
        return self.request("rastreio", body, **options)
