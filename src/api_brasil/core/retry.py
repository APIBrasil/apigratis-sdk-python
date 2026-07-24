"""Política de retry do cliente.

Por padrão a SDK tenta novamente apenas em HTTP 429 (rate limit) e em falhas
de conexão — nunca em timeouts ou erros de negócio, para não duplicar
cobranças/envios.
"""

from __future__ import annotations

import random
import time
from typing import Any, Dict, Optional, Union

__all__ = ["DEFAULT_RETRY", "resolve_retry", "backoff_delay_ms", "sleep_ms"]

#: Configuração padrão de retry.
#:
#: - ``retries``: novas tentativas além da original
#: - ``min_delay_ms``: atraso base do backoff exponencial
#: - ``max_delay_ms``: teto do atraso entre tentativas
#: - ``retry_on_statuses``: status HTTP que disparam retry
DEFAULT_RETRY: Dict[str, Any] = {
    "retries": 2,
    "min_delay_ms": 300,
    "max_delay_ms": 5000,
    "retry_on_statuses": [429],
}


def resolve_retry(
    config: Union[Dict[str, Any], bool, None] = None
) -> Optional[Dict[str, Any]]:
    """Normaliza a configuração de retry. ``False`` desativa completamente."""
    if config is False:
        return None

    resolved = dict(DEFAULT_RETRY)

    if isinstance(config, dict):
        resolved.update(
            {key: value for key, value in config.items() if value is not None}
        )

    return resolved


def backoff_delay_ms(attempt: int, retry: Dict[str, Any]) -> int:
    """Backoff exponencial com jitter: ``min * 2^attempt``, limitado a ``max``."""
    exponential = retry["min_delay_ms"] * (2**attempt)
    jitter = 0.5 + random.random() * 0.5

    return int(min(retry["max_delay_ms"], round(exponential * jitter)))


def sleep_ms(ms: int) -> None:
    """Pausa a execução por ``ms`` milissegundos."""
    if ms > 0:
        time.sleep(ms / 1000)
