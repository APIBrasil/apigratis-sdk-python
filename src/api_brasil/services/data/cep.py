"""CEP + geolocalização (device-based)."""

from __future__ import annotations

from typing import Any

from ...core.http import HttpClient
from ...core.types import Json
from ..device_proxy import DeviceProxyService

__all__ = ["CepService"]


class CepService(DeviceProxyService):
    """CEP + geolocalização (device-based): ``/cep/{action}``."""

    def __init__(self, http: HttpClient) -> None:
        super().__init__(http, "cep")

    def cep(self, body: Json, **options: Any) -> Any:
        """Consulta um CEP: ``POST /cep/cep`` body ``{"cep": ...}``."""
        return self.request("cep", body, **options)
