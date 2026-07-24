"""Relatórios e dashboard de consumo."""

from __future__ import annotations

from typing import Any, Optional

from ...core.http import HttpClient
from ...core.types import Json

__all__ = ["ReportsService"]


class ReportsService:
    """Relatórios e dashboard de consumo (``/reports/*``, ``/dashboard/stats``)."""

    def __init__(self, http: HttpClient) -> None:
        self.http = http

    def dashboard_stats(self, **options: Any) -> Any:
        """Estatísticas do dashboard: ``GET /dashboard/stats``."""
        return self.http.get("/dashboard/stats", **options)

    def consumption(self, **options: Any) -> Any:
        """Consumo: ``GET /reports/consumption``."""
        return self.http.get("/reports/consumption", **options)

    def generate_consumption_report(
        self, body: Optional[Json] = None, **options: Any
    ) -> Any:
        """Gera relatório de consumo: ``POST /reports/generate-consumption-report``."""
        return self.http.post("/reports/generate-consumption-report", body, **options)

    def extract(self, **options: Any) -> Any:
        """Extrato: ``GET /reports/extract``."""
        return self.http.get("/reports/extract", **options)

    def dashboard(self, **options: Any) -> Any:
        """Dashboard de relatórios: ``GET /reports/dashboard``."""
        return self.http.get("/reports/dashboard", **options)

    def summary(self, **options: Any) -> Any:
        """Resumo: ``GET /reports/summary``."""
        return self.http.get("/reports/summary", **options)

    def daily_usage(self, **options: Any) -> Any:
        """Uso diário: ``GET /reports/daily-usage``."""
        return self.http.get("/reports/daily-usage", **options)

    def monthly_summary(self, **options: Any) -> Any:
        """Resumo mensal: ``GET /reports/monthly-summary``."""
        return self.http.get("/reports/monthly-summary", **options)

    def error_analysis(self, **options: Any) -> Any:
        """Análise de erros: ``GET /reports/error-analysis``."""
        return self.http.get("/reports/error-analysis", **options)

    def device_analysis(self, **options: Any) -> Any:
        """Análise por device: ``GET /reports/device-analysis``."""
        return self.http.get("/reports/device-analysis", **options)

    def recent_requests(self, **options: Any) -> Any:
        """Requisições recentes: ``GET /reports/recent-requests``."""
        return self.http.get("/reports/recent-requests", **options)

    def quick_stats(self, **options: Any) -> Any:
        """Estatísticas rápidas: ``GET /reports/quick-stats``."""
        return self.http.get("/reports/quick-stats", **options)
