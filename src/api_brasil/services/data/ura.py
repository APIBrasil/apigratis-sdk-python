"""URA reversa / ligações."""

from __future__ import annotations

from typing import Any

from ...core.http import HttpClient
from ...core.types import Json

__all__ = ["UraService"]


class UraService:
    """URA reversa / ligações: ``/ura/call/*``."""

    def __init__(self, http: HttpClient) -> None:
        self.http = http

    def dialler(self, body: Json, **options: Any) -> Any:
        """Disca uma ligação: ``POST /ura/call/dialler``."""
        return self.http.post("/ura/call/dialler", body, **options)

    def status(self, body: Json, **options: Any) -> Any:
        """Consulta status da ligação: ``POST /ura/call/status``."""
        return self.http.post("/ura/call/status", body, **options)
