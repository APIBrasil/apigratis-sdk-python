"""Tabela FIPE (device-based)."""

from __future__ import annotations

from ...core.http import HttpClient
from ..device_proxy import DeviceProxyService

__all__ = ["FipeService"]


class FipeService(DeviceProxyService):
    """Tabela FIPE (device-based): ``/fipe/{action}``.

    Actions: ``ConsultarMarcas``, ``ConsultarModelos``, ``ConsultarAnoModelo``,
    ``ConsultarTabelaDeReferencia``, ``ConsultarValorComTodosParametros``...
    Use :meth:`~api_brasil.services.device_proxy.DeviceProxyService.request`.
    """

    def __init__(self, http: HttpClient) -> None:
        super().__init__(http, "fipe")
