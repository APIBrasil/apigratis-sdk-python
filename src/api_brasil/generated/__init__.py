"""Artefatos gerados do catálogo do gateway APIBrasil."""

from . import catalog
from .catalog import (
    CONSULTA_SERVICOS,
    CONSULTA_TIPOS,
    EVOLUTION_PATHS,
    SERVICE_ACTIONS,
    WHATSAPP_ACTIONS,
    WHATSMEOW_ACTIONS,
    consulta_tipo,
    service_actions,
)

__all__ = [
    "catalog",
    "WHATSAPP_ACTIONS",
    "EVOLUTION_PATHS",
    "WHATSMEOW_ACTIONS",
    "CONSULTA_SERVICOS",
    "CONSULTA_TIPOS",
    "SERVICE_ACTIONS",
    "consulta_tipo",
    "service_actions",
]
