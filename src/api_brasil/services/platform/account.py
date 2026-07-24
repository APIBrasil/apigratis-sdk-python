"""Conta, saldo, faturas, notificações e tickets."""

from __future__ import annotations

from typing import Any, Optional, Union

from ...core.http import HttpClient
from ...core.types import Json

__all__ = ["AccountService"]


class AccountService:
    """Conta, saldo, faturas, notificações e tickets."""

    def __init__(self, http: HttpClient) -> None:
        self.http = http

    def balance(self, **options: Any) -> Any:
        """Saldo/créditos da conta: ``GET /balance``."""
        return self.http.get("/balance", **options)

    def plan(self, **options: Any) -> Any:
        """Plano atual: ``GET /plan``."""
        return self.http.get("/plan", **options)

    def invoices(self, **options: Any) -> Any:
        """Faturas: ``GET /invoices``."""
        return self.http.get("/invoices", **options)

    def invoice_notes(self, **options: Any) -> Any:
        """Notas fiscais das faturas: ``GET /invoices/notes``."""
        return self.http.get("/invoices/notes", **options)

    def pay_invoice(self, body: Json, **options: Any) -> Any:
        """Paga uma fatura: ``POST /invoices/pay``."""
        return self.http.post("/invoices/pay", body, **options)

    def requests(self, body: Optional[Json] = None, **options: Any) -> Any:
        """Histórico de requisições da conta: ``POST /requests``."""
        return self.http.post("/requests", body, **options)

    def api_requests(self, body: Optional[Json] = None, **options: Any) -> Any:
        """Histórico de requisições por API: ``POST /api/requests``."""
        return self.http.post("/api/requests", body, **options)

    def jobs(self, **options: Any) -> Any:
        """Jobs em fila do usuário: ``GET /jobs``."""
        return self.http.get("/jobs", **options)

    def credentials(self, **options: Any) -> Any:
        """Credenciais do usuário: ``GET /credentials``."""
        return self.http.get("/credentials", **options)

    def indications(self, **options: Any) -> Any:
        """Indicações do usuário: ``GET /indications``."""
        return self.http.get("/indications", **options)

    def notifications(self, **options: Any) -> Any:
        """Notificações: ``GET /notifications``."""
        return self.http.get("/notifications", **options)

    def mark_notification_read(self, id: Union[str, int], **options: Any) -> Any:
        """Marca uma notificação como lida: ``PATCH /notifications/{id}/read``."""
        return self.http.patch("/notifications/{}/read".format(id), None, **options)

    def mark_all_notifications_read(self, **options: Any) -> Any:
        """Marca todas as notificações como lidas: ``POST /notifications/mark-all-read``."""
        return self.http.post("/notifications/mark-all-read", None, **options)

    def tickets(self, **options: Any) -> Any:
        """Tickets de suporte: ``GET /tickets``."""
        return self.http.get("/tickets", **options)

    def create_ticket(self, body: Json, **options: Any) -> Any:
        """Abre um ticket: ``POST /ticket``."""
        return self.http.post("/ticket", body, **options)

    def update_ticket(self, id: Union[str, int], body: Json, **options: Any) -> Any:
        """Atualiza um ticket: ``PUT /ticket/{id}``."""
        return self.http.put("/ticket/{}".format(id), body, **options)

    def ticket_messages(self, id: Union[str, int], **options: Any) -> Any:
        """Mensagens de um ticket: ``GET /ticket/{id}/messages``."""
        return self.http.get("/ticket/{}/messages".format(id), **options)

    def add_ticket_message(
        self, id: Union[str, int], body: Json, **options: Any
    ) -> Any:
        """Responde um ticket: ``POST /ticket/{id}/messages``."""
        return self.http.post("/ticket/{}/messages".format(id), body, **options)
