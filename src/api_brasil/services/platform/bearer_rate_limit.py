"""Rate limit por Bearer Token."""

from __future__ import annotations

from typing import Any

from ...core.http import HttpClient
from ...core.types import Json

__all__ = ["BearerRateLimitService"]


class BearerRateLimitService:
    """Rate limit por Bearer Token (``/bearer-rate-limit``)."""

    def __init__(self, http: HttpClient) -> None:
        self.http = http

    def get(self, **options: Any) -> Any:
        """Limite atual: ``GET /bearer-rate-limit``."""
        return self.http.get("/bearer-rate-limit", **options)

    def set(self, body: Json, **options: Any) -> Any:
        """Define o limite por minuto: ``PUT /bearer-rate-limit``."""
        return self.http.put("/bearer-rate-limit", body, **options)
