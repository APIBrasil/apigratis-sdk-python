"""WhatsMeow API (device-based)."""

from __future__ import annotations

from typing import Any, Optional

from ...core.http import HttpClient
from ...core.types import Json

__all__ = ["WhatsMeowService"]


class WhatsMeowService:
    """WhatsMeow API (device-based): ``POST /whatsmeow/{action}``.

    Exige ``Authorization: Bearer`` + ``DeviceToken``. As actions documentadas
    estão em :data:`api_brasil.generated.catalog.WHATSMEOW_ACTIONS`.
    """

    def __init__(self, http: HttpClient) -> None:
        self.http = http

    def request(self, action: str, body: Optional[Json] = None, **options: Any) -> Any:
        """Executa ``POST /whatsmeow/{action}``."""
        return self.http.post("/whatsmeow/" + action.lstrip("/"), body, **options)

    def queue(self, action: str, body: Optional[Json] = None, **options: Any) -> Any:
        """Executa a mesma chamada de forma assíncrona via fila."""
        return self.http.post(
            "/whatsmeow/" + action.lstrip("/") + "/queue", body, **options
        )
