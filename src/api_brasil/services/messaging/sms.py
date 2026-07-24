"""API de SMS (device-based e por créditos)."""

from __future__ import annotations

from typing import Any

from ...core.http import HttpClient
from ...core.types import Json
from ..device_proxy import DeviceProxyService

__all__ = ["SmsService"]


class SmsService(DeviceProxyService):
    """API de SMS (device-based): ``POST /sms/{action}``.

    Exige ``Authorization: Bearer`` + ``DeviceToken``.
    """

    def __init__(self, http: HttpClient) -> None:
        super().__init__(http, "sms")

    def send(self, body: Json, **options: Any) -> Any:
        """Envia um SMS pelo device: ``POST /sms/send``.

        Campos: ``number``, ``message``, ``operator``, ``user_reply``,
        ``webhook_url``.
        """
        return self.request("send", body, **options)

    def send_with_credits(self, body: Json, **options: Any) -> Any:
        """Envia um SMS debitando créditos da conta (sem DeviceToken).

        ``POST /sms/send/credits``
        """
        return self.http.post("/sms/send/credits", body, **options)
