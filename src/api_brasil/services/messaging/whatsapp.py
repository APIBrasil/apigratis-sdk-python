"""API de WhatsApp (device-based)."""

from __future__ import annotations

from typing import Any, Optional

from ...core.http import HttpClient
from ...core.types import Json
from ..device_proxy import DeviceProxyService

__all__ = ["WhatsAppService"]


class WhatsAppService(DeviceProxyService):
    """API de WhatsApp (device-based): ``POST /whatsapp/{action}``.

    Exige ``Authorization: Bearer`` + ``DeviceToken``.

    Além dos métodos nomeados, :meth:`request` aceita qualquer action do
    catálogo (:data:`api_brasil.generated.catalog.WHATSAPP_ACTIONS`).
    """

    def __init__(self, http: HttpClient) -> None:
        super().__init__(http, "whatsapp")

    def start(self, body: Optional[Json] = None, **options: Any) -> Any:
        """Inicia a sessão do device (aceita webhooks opcionais).

        Webhooks: ``webhook_wh_status``, ``webhook_wh_message``,
        ``webhook_wh_connect``, ``webhook_wh_qrcode``.
        """
        return self.request("start", body, **options)

    def qrcode(self, body: Optional[Json] = None, **options: Any) -> Any:
        """Retorna o QR Code de pareamento (``response.qrcode`` em base64)."""
        return self.request("qrcode", body, **options)

    def logout(self, body: Optional[Json] = None, **options: Any) -> Any:
        """Encerra a sessão."""
        return self.request("logout", body, **options)

    def close(self, body: Optional[Json] = None, **options: Any) -> Any:
        """Fecha o navegador/sessão no servidor."""
        return self.request("close", body, **options)

    def delete_session(self, body: Optional[Json] = None, **options: Any) -> Any:
        """Apaga a sessão no servidor."""
        return self.request("deleteSession", body, **options)

    def send_text(self, body: Json, **options: Any) -> Any:
        """Envia mensagem de texto: ``{"number": "5511999999999", "text": "Olá!"}``."""
        return self.request("sendText", body, **options)

    def send_file(self, body: Json, **options: Any) -> Any:
        """Envia arquivo a partir de uma URL: ``{"number": ..., "path": ...}``."""
        return self.request("sendFile", body, **options)

    def send_file64(self, body: Json, **options: Any) -> Any:
        """Envia arquivo em base64."""
        return self.request("sendFile64", body, **options)

    def send_audio(self, body: Json, **options: Any) -> Any:
        """Envia áudio (URL; convertido para mp3 pelo gateway, máx. 6 min)."""
        return self.request("sendAudio", body, **options)

    def send_video(self, body: Json, **options: Any) -> Any:
        """Envia vídeo a partir de uma URL."""
        return self.request("sendVideo", body, **options)

    def send_link(self, body: Json, **options: Any) -> Any:
        """Envia um link com preview."""
        return self.request("sendLink", body, **options)

    def send_location(self, body: Json, **options: Any) -> Any:
        """Envia uma localização: ``{"number": ..., "lat": ..., "lng": ...}``."""
        return self.request("sendLocation", body, **options)

    def send_contact(self, body: Json, **options: Any) -> Any:
        """Envia um contato."""
        return self.request("sendContact", body, **options)

    def queue(self, action: str, body: Optional[Json] = None, **options: Any) -> Any:
        """Executa qualquer action de forma assíncrona via fila.

        ``POST /whatsapp/{action}/queue``
        """
        return self.http.post(
            "/whatsapp/{}/queue".format(action.strip("/")), body, **options
        )
