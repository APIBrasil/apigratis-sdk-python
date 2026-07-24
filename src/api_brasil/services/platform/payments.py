"""Pagamentos e recargas (PIX, boleto e cartão)."""

from __future__ import annotations

from typing import Any, List

from ...core.http import HttpClient
from ...core.types import Json

__all__ = ["PaymentsService"]


class PaymentsService:
    """Pagamentos e recargas — ``/recharge``, ``/{provider}/pix/*``,
    ``/{provider}/boleto/*``, ``/mercadopago/card/*``.
    """

    #: Provedores de pagamento suportados pelo gateway.
    PROVIDERS: List[str] = ["santander", "inter", "mercadopago", "sicoob"]

    def __init__(self, http: HttpClient) -> None:
        self.http = http

    def recharges(self, **options: Any) -> Any:
        """Lista as recargas: ``GET /recharges``."""
        return self.http.get("/recharges", **options)

    def recharge(self, body: Json, **options: Any) -> Any:
        """Cria uma recarga (pix|boleto): ``POST /recharge``.

        :param body: ``amount``, ``type``
        """
        return self.http.post("/recharge", body, **options)

    def recharge_show(self, identifier: str, **options: Any) -> Any:
        """Detalha uma recarga: ``GET /recharge/{identifier}``."""
        return self.http.get("/recharge/" + identifier, **options)

    def pix_generate(self, provider: str, body: Json, **options: Any) -> Any:
        """Gera uma cobrança PIX: ``POST /{provider}/pix/generate``.

        :param provider: um de :data:`PROVIDERS`
        """
        return self.http.post("/{}/pix/generate".format(provider), body, **options)

    def pix_status(self, provider: str, tx_id: str, **options: Any) -> Any:
        """Consulta uma cobrança PIX: ``GET /{provider}/pix/{tx_id}``."""
        return self.http.get("/{}/pix/{}".format(provider, tx_id), **options)

    def boleto_generate(self, provider: str, body: Json, **options: Any) -> Any:
        """Gera um boleto: ``POST /{provider}/boleto/generate``."""
        return self.http.post("/{}/boleto/generate".format(provider), body, **options)

    def boleto_status(self, provider: str, id: str, **options: Any) -> Any:
        """Consulta um boleto: ``GET /{provider}/boleto/{id}``."""
        return self.http.get("/{}/boleto/{}".format(provider, id), **options)

    def boleto_pdf(self, provider: str, id: str, **options: Any) -> Any:
        """Baixa o PDF de um boleto: ``GET /{provider}/boleto/{id}/pdf``.

        Devolve o conteúdo binário do arquivo (``bytes``).
        """
        options.setdefault("response_type", "raw")

        return self.http.get("/{}/boleto/{}/pdf".format(provider, id), **options)

    def card_process(self, body: Json, **options: Any) -> Any:
        """Processa pagamento com cartão (Mercado Pago): ``POST /mercadopago/card/process``."""
        return self.http.post("/mercadopago/card/process", body, **options)

    def card_installments(self, body: Json, **options: Any) -> Any:
        """Consulta parcelas do cartão: ``POST /mercadopago/card/installments``."""
        return self.http.post("/mercadopago/card/installments", body, **options)

    def card_status(self, id: str, **options: Any) -> Any:
        """Consulta um pagamento de cartão: ``GET /mercadopago/card/{id}``."""
        return self.http.get("/mercadopago/card/" + id, **options)

    def checkout_payment_methods(self, **options: Any) -> Any:
        """Métodos de pagamento do checkout: ``GET /checkout/payment-methods``."""
        return self.http.get("/checkout/payment-methods", **options)

    def checkout_periods(self, **options: Any) -> Any:
        """Períodos do checkout: ``GET /checkout/periods``."""
        return self.http.get("/checkout/periods", **options)

    def validate_coupon(self, body: Json, **options: Any) -> Any:
        """Valida um cupom: ``POST /checkout/validate-coupon``."""
        return self.http.post("/checkout/validate-coupon", body, **options)

    def checkout_finalize(self, body: Json, **options: Any) -> Any:
        """Finaliza o checkout: ``POST /checkout/finalize``."""
        return self.http.post("/checkout/finalize", body, **options)
