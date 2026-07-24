"""Chip virtual."""

from __future__ import annotations

from typing import Any, Optional

from ...core.http import HttpClient
from ...core.types import Json

__all__ = ["ChipVirtualService"]


class ChipVirtualService:
    """Chip virtual: ``/chip/virtual/*``."""

    def __init__(self, http: HttpClient) -> None:
        self.http = http

    def operators(self, body: Optional[Json] = None, **options: Any) -> Any:
        """Lista operadoras: ``POST /chip/virtual/operators``."""
        return self.http.post("/chip/virtual/operators", body, **options)

    def buy(self, body: Json, **options: Any) -> Any:
        """Compra um número: ``POST /chip/virtual/buy``."""
        return self.http.post("/chip/virtual/buy", body, **options)

    def activation(self, body: Json, **options: Any) -> Any:
        """Consulta ativação: ``POST /chip/virtual/activation``."""
        return self.http.post("/chip/virtual/activation", body, **options)

    def services(self, body: Optional[Json] = None, **options: Any) -> Any:
        """Lista serviços: ``POST /chip/virtual/services``."""
        return self.http.post("/chip/virtual/services", body, **options)
