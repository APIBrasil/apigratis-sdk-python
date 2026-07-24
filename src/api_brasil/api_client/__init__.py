"""Cliente HTTP legado (<= 2.0.x) — mantido por compatibilidade.

.. deprecated:: 2.0.1
   Prefira :class:`api_brasil.ApiBrasil` / :class:`api_brasil.HttpClient`.
"""

from .client_builder import APIBrasilClient

__all__ = ["APIBrasilClient"]
