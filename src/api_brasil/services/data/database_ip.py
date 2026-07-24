"""GeoIP (device-based)."""

from __future__ import annotations

from typing import Any, Optional

from ...core.http import HttpClient
from ...core.types import Json

__all__ = ["DatabaseIpService"]


class DatabaseIpService:
    """GeoIP (device-based): ``POST /database/ip``."""

    def __init__(self, http: HttpClient) -> None:
        self.http = http

    def ip(self, body: Optional[Json] = None, **options: Any) -> Any:
        """Consulta a base de IPs: ``POST /database/ip`` body ``{"ip": ...}``."""
        return self.http.post("/database/ip", body, **options)
