"""IP Whitelist da conta."""

from __future__ import annotations

from typing import Any, List, Union

from ...core.http import HttpClient

__all__ = ["IpWhitelistService"]


class IpWhitelistService:
    """IP Whitelist da conta (``/ip-whitelist/*``).

    Restringe de quais IPs o Bearer Token pode ser usado.
    """

    def __init__(self, http: HttpClient) -> None:
        self.http = http

    def get(self, **options: Any) -> Any:
        """Configuração atual: ``GET /ip-whitelist``."""
        return self.http.get("/ip-whitelist", **options)

    def set(self, ip_whitelist: Union[str, List[str]], **options: Any) -> Any:
        """Substitui a lista inteira: ``PUT /ip-whitelist``."""
        return self.http.put("/ip-whitelist", {"ip_whitelist": ip_whitelist}, **options)

    def add(self, entry: str, **options: Any) -> Any:
        """Adiciona uma entrada: ``POST /ip-whitelist/add``."""
        return self.http.post("/ip-whitelist/add", {"entry": entry}, **options)

    def remove(self, entry: str, **options: Any) -> Any:
        """Remove uma entrada: ``DELETE /ip-whitelist/remove``."""
        return self.http.delete("/ip-whitelist/remove", {"entry": entry}, **options)

    def add_current(self, **options: Any) -> Any:
        """Adiciona o IP atual: ``POST /ip-whitelist/add-current``."""
        return self.http.post("/ip-whitelist/add-current", None, **options)

    def reset(self, **options: Any) -> Any:
        """Libera todos os IPs (wildcard): ``POST /ip-whitelist/reset``."""
        return self.http.post("/ip-whitelist/reset", None, **options)

    def validate(self, entry: str, **options: Any) -> Any:
        """Valida uma entrada: ``POST /ip-whitelist/validate``."""
        return self.http.post("/ip-whitelist/validate", {"entry": entry}, **options)

    def current_ip(self, **options: Any) -> Any:
        """IP atual visto pelo gateway: ``GET /ip-whitelist/current-ip``."""
        return self.http.get("/ip-whitelist/current-ip", **options)
