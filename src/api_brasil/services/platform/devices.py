"""Gestão de devices."""

from __future__ import annotations

from typing import Any, Optional

from ...core.http import HttpClient
from ...core.types import Json

__all__ = ["DevicesService"]


class DevicesService:
    """Gestão de devices (``/devices/*``).

    Devices são a credencial de consumo dos serviços device-based: crie um
    device com a ``SecretKey`` da API desejada e use o ``device_token``
    retornado como header ``DeviceToken``.
    """

    def __init__(self, http: HttpClient) -> None:
        self.http = http

    def list(self, query: Optional[Json] = None, **options: Any) -> Any:
        """Lista os devices do usuário: ``GET /devices``.

        :param query: ex: ``{"paginate": True}``
        """
        options["query"] = {**(query or {}), **(options.get("query") or {})}

        return self.http.get("/devices", **options)

    def store(self, body: Json, **options: Any) -> Any:
        """Cria um device: ``POST /devices/store``.

        A ``SecretKey`` da API (painel APIBrasil) vai no header — passe em
        ``secret_key=...`` ou configure ``secret_key`` no cliente.

        :param body: ``device_name``, ``type``, ``device_key``, webhooks...
        """
        secret_key = options.get("secret_key") or self.http.secret_key
        if secret_key is not None:
            options["secret_key"] = secret_key

        return self.http.post("/devices/store", body, **options)

    def show(self, device_token: Optional[str] = None, **options: Any) -> Any:
        """Detalha um device: ``GET /devices/show?search={device_token}``."""
        search = device_token if device_token is not None else self.http.device_token
        options["query"] = {"search": search, **(options.get("query") or {})}

        return self.http.get("/devices/show", **options)

    def update(self, body: Json, **options: Any) -> Any:
        """Atualiza um device: ``POST /devices/update``.

        Body com ``device_token`` + campos a alterar.
        """
        return self.http.post("/devices/update", body, **options)

    def destroy(self, device_token: Optional[str] = None, **options: Any) -> Any:
        """Remove um device: ``DELETE /devices/destroy``."""
        search = device_token if device_token is not None else self.http.device_token

        return self.http.delete("/devices/destroy", {"search": search}, **options)

    def requests(self, body: Optional[Json] = None, **options: Any) -> Any:
        """Histórico de requisições do device: ``POST /devices/requests``."""
        return self.http.post("/devices/requests", body, **options)
