"""Catálogo público da plataforma."""

from __future__ import annotations

from typing import Any, Optional
from urllib.parse import quote

from ...core.http import HttpClient
from ...core.types import Json

__all__ = ["CatalogService"]


class CatalogService:
    """Catálogo público: APIs, planos, documentações e servidores.

    A maioria das rotas é pública (não exige Bearer Token).
    """

    def __init__(self, http: HttpClient) -> None:
        self.http = http

    def apis(self, search: Optional[str] = None, **options: Any) -> Any:
        """Lista/busca APIs disponíveis: ``GET /apis?search=``."""
        options["query"] = {
            **({"search": search} if search else {}),
            **(options.get("query") or {}),
        }

        return self.http.get("/apis", **options)

    def api(self, identifier: str, **options: Any) -> Any:
        """Detalha uma API por identificador: ``GET /apis/{identifier}``."""
        return self.http.get("/apis/" + identifier, **options)

    def api_by_name(self, name: str, **options: Any) -> Any:
        """Detalha uma API pelo nome: ``GET /apis/name/{name}``."""
        return self.http.get("/apis/name/" + quote(name, safe=""), **options)

    def api_categories(self, **options: Any) -> Any:
        """Categorias de APIs: ``GET /apis/categories``."""
        return self.http.get("/apis/categories", **options)

    def my_apis(self, **options: Any) -> Any:
        """APIs contratadas pelo usuário (autenticado): ``GET /apis/list``."""
        return self.http.get("/apis/list", **options)

    def apis_by_device(self, device_token: str, **options: Any) -> Any:
        """APIs vinculadas a um device: ``GET /apis/device/{device_token}``."""
        return self.http.get("/apis/device/" + device_token, **options)

    def plans(self, **options: Any) -> Any:
        """Planos disponíveis: ``GET /plans``."""
        return self.http.get("/plans", **options)

    def documentations(self, **options: Any) -> Any:
        """Documentações: ``GET /documentations``."""
        return self.http.get("/documentations", **options)

    def documentations_by_server(self, server_search: str, **options: Any) -> Any:
        """Documentação por servidor: ``GET /documentations/server/{server_search}``."""
        return self.http.get("/documentations/server/" + server_search, **options)

    def servers(self, **options: Any) -> Any:
        """Servidores disponíveis: ``GET /servers``."""
        return self.http.get("/servers", **options)

    def endpoint_url(self, body: Json, **options: Any) -> Any:
        """Resolve a URL de uma action: ``POST /endpoint/url``.

        Descoberta dinâmica de endpoints.
        """
        return self.http.post("/endpoint/url", body, **options)

    def endpoint_body(self, body: Json, **options: Any) -> Any:
        """Body esperado por uma action: ``POST /endpoint/body``."""
        return self.http.post("/endpoint/body", body, **options)

    def status(self, **options: Any) -> Any:
        """Status do gateway: ``GET /status``."""
        return self.http.get("/status", **options)
