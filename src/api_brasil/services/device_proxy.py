"""Base dos serviços "device-based" do gateway."""

from __future__ import annotations

from typing import Any, Optional

from ..core.http import HttpClient
from ..core.types import Json

__all__ = ["DeviceProxyService"]


class DeviceProxyService:
    """Base dos serviços device-based (``/api/v2/{servico}/{action}``).

    Exigem ``Authorization: Bearer`` + header ``DeviceToken``.

    Todos expõem :meth:`request` como porta de saída genérica — as actions são
    dinâmicas por provedor, consulte a documentação em https://doc.apibrasil.io

    A resposta segue o envelope device-based
    (``{"error": ..., "message": ..., "response": ...}``).
    """

    def __init__(self, http: HttpClient, service: str) -> None:
        self.http = http
        #: Nome do serviço no gateway (primeiro segmento da rota).
        self.service = service

    def request(self, action: str, body: Optional[Json] = None, **options: Any) -> Any:
        """Executa uma action do serviço: ``POST /{servico}/{action}``."""
        return self.http.post(
            "/{}/{}".format(self.service, action.strip("/")), body, **options
        )
