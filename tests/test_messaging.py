"""Testes de rota dos serviços de mensageria."""

from __future__ import annotations

import pytest

from api_brasil import ApiBrasil

from .helpers import assert_route

CASOS = [
    # WhatsApp — métodos nomeados
    (
        lambda api: api.whatsapp.start({"webhook_wh_message": "u"}),
        "/whatsapp/start",
        "POST",
    ),
    (lambda api: api.whatsapp.qrcode(), "/whatsapp/qrcode", "POST"),
    (lambda api: api.whatsapp.logout(), "/whatsapp/logout", "POST"),
    (lambda api: api.whatsapp.close(), "/whatsapp/close", "POST"),
    (lambda api: api.whatsapp.delete_session(), "/whatsapp/deleteSession", "POST"),
    (
        lambda api: api.whatsapp.send_text({"number": "55", "text": "oi"}),
        "/whatsapp/sendText",
        "POST",
    ),
    (
        lambda api: api.whatsapp.send_file({"number": "55", "path": "u"}),
        "/whatsapp/sendFile",
        "POST",
    ),
    (
        lambda api: api.whatsapp.send_file64({"number": "55"}),
        "/whatsapp/sendFile64",
        "POST",
    ),
    (
        lambda api: api.whatsapp.send_audio({"number": "55"}),
        "/whatsapp/sendAudio",
        "POST",
    ),
    (
        lambda api: api.whatsapp.send_video({"number": "55"}),
        "/whatsapp/sendVideo",
        "POST",
    ),
    (
        lambda api: api.whatsapp.send_link({"number": "55"}),
        "/whatsapp/sendLink",
        "POST",
    ),
    (
        lambda api: api.whatsapp.send_location({"number": "55"}),
        "/whatsapp/sendLocation",
        "POST",
    ),
    (
        lambda api: api.whatsapp.send_contact({"number": "55"}),
        "/whatsapp/sendContact",
        "POST",
    ),
    # WhatsApp — genéricos
    (
        lambda api: api.whatsapp.request("getConnectionState"),
        "/whatsapp/getConnectionState",
        "POST",
    ),
    (
        lambda api: api.whatsapp.queue("sendText", {"number": "55"}),
        "/whatsapp/sendText/queue",
        "POST",
    ),
    # Evolution
    (
        lambda api: api.evolution.request("message", "sendText", {"x": 1}),
        "/evolution/message/sendText",
        "POST",
    ),
    (
        lambda api: api.evolution.call("instance/create", {"x": 1}),
        "/evolution/instance/create",
        "POST",
    ),
    (
        lambda api: api.evolution.queue("message", "sendText", {"x": 1}),
        "/evolution/message/sendText/queue",
        "POST",
    ),
    # WhatsMeow
    (
        lambda api: api.whatsmeow.request("send/text", {"x": 1}),
        "/whatsmeow/send/text",
        "POST",
    ),
    (
        lambda api: api.whatsmeow.queue("send/text", {"x": 1}),
        "/whatsmeow/send/text/queue",
        "POST",
    ),
    # SMS
    (
        lambda api: api.sms.send({"number": "55", "message": "oi"}),
        "/sms/send",
        "POST",
    ),
    (
        lambda api: api.sms.send_with_credits({"number": "55", "message": "oi"}),
        "/sms/send/credits",
        "POST",
    ),
]


@pytest.mark.parametrize("call,path,method", CASOS)
def test_rota(call, path, method):
    assert_route(call, path, method)


def test_send_text_envia_o_body():
    assert_route(
        lambda api: api.whatsapp.send_text({"number": "5511999999999", "text": "Olá!"}),
        "/whatsapp/sendText",
        "POST",
        {"number": "5511999999999", "text": "Olá!"},
    )
