"""Execução em lote."""

from __future__ import annotations

from typing import Any

from ...core.http import HttpClient
from ...core.types import Json

__all__ = ["BulkService"]


class BulkService:
    """Execução em lote: ``/bulk/direct/{action}`` e ``/bulk/queue/{action}``."""

    def __init__(self, http: HttpClient) -> None:
        self.http = http

    def direct(self, action: str, body: Json, **options: Any) -> Any:
        """Executa um lote de forma síncrona: ``POST /bulk/direct/{action}``."""
        return self.http.post("/bulk/direct/" + action.lstrip("/"), body, **options)

    def queue(self, action: str, body: Json, **options: Any) -> Any:
        """Enfileira um lote: ``POST /bulk/queue/{action}``."""
        return self.http.post("/bulk/queue/" + action.lstrip("/"), body, **options)
