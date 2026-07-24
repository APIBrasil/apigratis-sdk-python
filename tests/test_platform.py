"""Testes de rota dos serviços de plataforma."""

from __future__ import annotations

import pytest

from api_brasil import ApiBrasil

from .helpers import BASE, assert_route, build_api, ok

CASOS = [
    # Auth
    (
        lambda api: api.auth.login({"email": "a", "password": "b"}),
        "/auth/login",
        "POST",
    ),
    (lambda api: api.auth.send_2fa({"challenge": "c"}), "/auth/2fa/send", "POST"),
    (lambda api: api.auth.verify_2fa({"code": "0"}), "/auth/login/verify-2fa", "POST"),
    (lambda api: api.auth.two_factor_methods(), "/auth/2fa/methods", "GET"),
    (lambda api: api.auth.register({"email": "a"}), "/auth/register", "POST"),
    (
        lambda api: api.auth.register_simple({"email": "a"}),
        "/auth/register/simple",
        "POST",
    ),
    (
        lambda api: api.auth.verification_send({"type": "email"}),
        "/auth/verification/send",
        "POST",
    ),
    (
        lambda api: api.auth.verification_verify({"code": "0"}),
        "/auth/verification/verify",
        "POST",
    ),
    (
        lambda api: api.auth.password_forgot({"identifier": "a"}),
        "/auth/password/forgot",
        "POST",
    ),
    (
        lambda api: api.auth.password_verify_code({"code": "0"}),
        "/auth/password/verify-code",
        "POST",
    ),
    (
        lambda api: api.auth.password_reset({"reset_token": "t"}),
        "/auth/password/reset",
        "POST",
    ),
    (
        lambda api: api.auth.password_resend({"identifier": "a"}),
        "/auth/password/resend",
        "POST",
    ),
    (
        lambda api: api.auth.change_password({"password": "x"}),
        "/password/change",
        "POST",
    ),
    (lambda api: api.auth.profile(), "/profile", "POST"),
    (lambda api: api.auth.me(), "/profile/me", "GET"),
    (lambda api: api.auth.update_me({"name": "x"}), "/profile/me", "PUT"),
    (lambda api: api.auth.verify(), "/auth/verify", "GET"),
    (lambda api: api.auth.refresh(), "/refresh", "POST"),
    (lambda api: api.auth.token_rotate(), "/auth/token/rotate", "POST"),
    (lambda api: api.auth.token_revoke(), "/auth/token/revoke", "POST"),
    (lambda api: api.auth.logout(), "/auth/logout", "POST"),
    # Devices
    (lambda api: api.devices.list(), "/devices", "GET"),
    (lambda api: api.devices.store({"device_name": "x"}), "/devices/store", "POST"),
    (lambda api: api.devices.show("tok"), "/devices/show?search=tok", "GET"),
    (lambda api: api.devices.update({"device_token": "t"}), "/devices/update", "POST"),
    (lambda api: api.devices.destroy("tok"), "/devices/destroy", "DELETE"),
    (lambda api: api.devices.requests(), "/devices/requests", "POST"),
    # Account
    (lambda api: api.account.balance(), "/balance", "GET"),
    (lambda api: api.account.plan(), "/plan", "GET"),
    (lambda api: api.account.invoices(), "/invoices", "GET"),
    (lambda api: api.account.invoice_notes(), "/invoices/notes", "GET"),
    (lambda api: api.account.pay_invoice({"id": 1}), "/invoices/pay", "POST"),
    (lambda api: api.account.requests(), "/requests", "POST"),
    (lambda api: api.account.api_requests(), "/api/requests", "POST"),
    (lambda api: api.account.jobs(), "/jobs", "GET"),
    (lambda api: api.account.credentials(), "/credentials", "GET"),
    (lambda api: api.account.indications(), "/indications", "GET"),
    (lambda api: api.account.notifications(), "/notifications", "GET"),
    (
        lambda api: api.account.mark_notification_read(7),
        "/notifications/7/read",
        "PATCH",
    ),
    (
        lambda api: api.account.mark_all_notifications_read(),
        "/notifications/mark-all-read",
        "POST",
    ),
    (lambda api: api.account.tickets(), "/tickets", "GET"),
    (lambda api: api.account.create_ticket({"subject": "x"}), "/ticket", "POST"),
    (lambda api: api.account.update_ticket(3, {"x": 1}), "/ticket/3", "PUT"),
    (lambda api: api.account.ticket_messages(3), "/ticket/3/messages", "GET"),
    (
        lambda api: api.account.add_ticket_message(3, {"x": 1}),
        "/ticket/3/messages",
        "POST",
    ),
    # Payments
    (lambda api: api.payments.recharges(), "/recharges", "GET"),
    (lambda api: api.payments.recharge({"amount": 100}), "/recharge", "POST"),
    (lambda api: api.payments.recharge_show("id1"), "/recharge/id1", "GET"),
    (
        lambda api: api.payments.pix_generate("inter", {"amount": 100}),
        "/inter/pix/generate",
        "POST",
    ),
    (lambda api: api.payments.pix_status("inter", "tx1"), "/inter/pix/tx1", "GET"),
    (
        lambda api: api.payments.boleto_generate("sicoob", {"amount": 1}),
        "/sicoob/boleto/generate",
        "POST",
    ),
    (
        lambda api: api.payments.boleto_status("sicoob", "b1"),
        "/sicoob/boleto/b1",
        "GET",
    ),
    (
        lambda api: api.payments.boleto_pdf("sicoob", "b1"),
        "/sicoob/boleto/b1/pdf",
        "GET",
    ),
    (
        lambda api: api.payments.card_process({"x": 1}),
        "/mercadopago/card/process",
        "POST",
    ),
    (
        lambda api: api.payments.card_installments({"x": 1}),
        "/mercadopago/card/installments",
        "POST",
    ),
    (lambda api: api.payments.card_status("c1"), "/mercadopago/card/c1", "GET"),
    (
        lambda api: api.payments.checkout_payment_methods(),
        "/checkout/payment-methods",
        "GET",
    ),
    (lambda api: api.payments.checkout_periods(), "/checkout/periods", "GET"),
    (
        lambda api: api.payments.validate_coupon({"code": "x"}),
        "/checkout/validate-coupon",
        "POST",
    ),
    (
        lambda api: api.payments.checkout_finalize({"x": 1}),
        "/checkout/finalize",
        "POST",
    ),
    # Catalog
    (lambda api: api.catalog.apis(), "/apis", "GET"),
    (lambda api: api.catalog.api("id1"), "/apis/id1", "GET"),
    (lambda api: api.catalog.api_by_name("whats app"), "/apis/name/whats%20app", "GET"),
    (lambda api: api.catalog.api_categories(), "/apis/categories", "GET"),
    (lambda api: api.catalog.my_apis(), "/apis/list", "GET"),
    (lambda api: api.catalog.apis_by_device("tok"), "/apis/device/tok", "GET"),
    (lambda api: api.catalog.plans(), "/plans", "GET"),
    (lambda api: api.catalog.documentations(), "/documentations", "GET"),
    (
        lambda api: api.catalog.documentations_by_server("s1"),
        "/documentations/server/s1",
        "GET",
    ),
    (lambda api: api.catalog.servers(), "/servers", "GET"),
    (lambda api: api.catalog.endpoint_url({"x": 1}), "/endpoint/url", "POST"),
    (lambda api: api.catalog.endpoint_body({"x": 1}), "/endpoint/body", "POST"),
    (lambda api: api.catalog.status(), "/status", "GET"),
    # Reports
    (lambda api: api.reports.dashboard_stats(), "/dashboard/stats", "GET"),
    (lambda api: api.reports.consumption(), "/reports/consumption", "GET"),
    (
        lambda api: api.reports.generate_consumption_report(),
        "/reports/generate-consumption-report",
        "POST",
    ),
    (lambda api: api.reports.extract(), "/reports/extract", "GET"),
    (lambda api: api.reports.dashboard(), "/reports/dashboard", "GET"),
    (lambda api: api.reports.summary(), "/reports/summary", "GET"),
    (lambda api: api.reports.daily_usage(), "/reports/daily-usage", "GET"),
    (lambda api: api.reports.monthly_summary(), "/reports/monthly-summary", "GET"),
    (lambda api: api.reports.error_analysis(), "/reports/error-analysis", "GET"),
    (lambda api: api.reports.device_analysis(), "/reports/device-analysis", "GET"),
    (lambda api: api.reports.recent_requests(), "/reports/recent-requests", "GET"),
    (lambda api: api.reports.quick_stats(), "/reports/quick-stats", "GET"),
    # IP whitelist
    (lambda api: api.ip_whitelist.get(), "/ip-whitelist", "GET"),
    (lambda api: api.ip_whitelist.set(["1.1.1.1"]), "/ip-whitelist", "PUT"),
    (lambda api: api.ip_whitelist.add("1.1.1.1"), "/ip-whitelist/add", "POST"),
    (lambda api: api.ip_whitelist.remove("1.1.1.1"), "/ip-whitelist/remove", "DELETE"),
    (lambda api: api.ip_whitelist.add_current(), "/ip-whitelist/add-current", "POST"),
    (lambda api: api.ip_whitelist.reset(), "/ip-whitelist/reset", "POST"),
    (
        lambda api: api.ip_whitelist.validate("1.1.1.1"),
        "/ip-whitelist/validate",
        "POST",
    ),
    (lambda api: api.ip_whitelist.current_ip(), "/ip-whitelist/current-ip", "GET"),
    # Bearer rate limit
    (lambda api: api.bearer_rate_limit.get(), "/bearer-rate-limit", "GET"),
    (lambda api: api.bearer_rate_limit.set({"limit": 60}), "/bearer-rate-limit", "PUT"),
]


@pytest.mark.parametrize("call,path,method", CASOS)
def test_rota(call, path, method):
    assert_route(call, path, method)


def test_login_guarda_o_token():
    transport, api = build_api()
    transport.respond_with(ok({"authorization": {"token": "novo-jwt"}}))

    api.auth.login({"email": "a", "password": "b"})

    assert api.http.bearer_token == "novo-jwt"


def test_logout_limpa_o_token():
    transport, api = build_api()
    api.auth.logout()

    assert api.http.bearer_token is None


def test_devices_store_usa_secret_key_do_cliente():
    transport, api = build_api(secret_key="segredo")
    api.devices.store({"device_name": "bot"})

    assert transport.last_headers["SecretKey"] == "segredo"


def test_boleto_pdf_pede_response_type_raw():
    transport, api = build_api()
    api.payments.boleto_pdf("sicoob", "b1")

    assert transport.last.response_type == "raw"
