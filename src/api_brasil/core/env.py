"""Leitura da configuração a partir das variáveis de ambiente."""

from __future__ import annotations

import os
from typing import Any, Dict

__all__ = ["ENV_VARS", "config_from_env"]

#: Variáveis de ambiente reconhecidas pela SDK.
ENV_VARS: Dict[str, str] = {
    "bearer_token": "APIBRASIL_BEARER_TOKEN",
    "device_token": "APIBRASIL_DEVICE_TOKEN",
    "secret_key": "APIBRASIL_SECRET_KEY",
    "base_url": "APIBRASIL_BASE_URL",
}


def config_from_env() -> Dict[str, Any]:
    """Lê a configuração das variáveis de ambiente (quando disponíveis).

    Valores passados explicitamente no construtor sempre têm prioridade.
    """
    config: Dict[str, Any] = {}

    for key, name in ENV_VARS.items():
        value = os.environ.get(name)
        if value:
            config[key] = value

    return config
