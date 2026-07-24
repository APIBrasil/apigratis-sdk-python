"""Evolution API (device-based)."""

from __future__ import annotations

from typing import Any, Optional

from ...core.http import HttpClient
from ...core.types import Json

__all__ = ["EvolutionService"]


class EvolutionService:
    """Evolution API (device-based): ``POST /evolution/{controller}/{action}``.

    Exige ``Authorization: Bearer`` + ``DeviceToken``.

    Exemplos de controller/action: ``instance/create``, ``message/sendText``.
    Os caminhos documentados estão em
    :data:`api_brasil.generated.catalog.EVOLUTION_PATHS`.
    """

    def __init__(self, http: HttpClient) -> None:
        self.http = http

    def request(
        self,
        controller: str,
        action: str,
        body: Optional[Json] = None,
        **options: Any,
    ) -> Any:
        """Executa ``POST /evolution/{controller}/{action}``."""
        return self.http.post(
            "/evolution/{}/{}".format(controller, action), body, **options
        )

    def call(self, path: str, body: Optional[Json] = None, **options: Any) -> Any:
        """Executa um caminho completo do catálogo: ``POST /evolution/{path}``."""
        return self.http.post("/evolution/" + path.lstrip("/"), body, **options)

    def queue(
        self,
        controller: str,
        action: str,
        body: Optional[Json] = None,
        **options: Any,
    ) -> Any:
        """Executa a mesma chamada de forma assíncrona via fila."""
        return self.http.post(
            "/evolution/{}/{}/queue".format(controller, action), body, **options
        )
