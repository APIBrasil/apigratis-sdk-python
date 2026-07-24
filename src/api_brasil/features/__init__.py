"""Interface legada (<= 2.0.x) — mantida por compatibilidade.

.. deprecated:: 2.0.1
   Prefira o cliente :class:`api_brasil.ApiBrasil`, que cobre toda a
   plataforma com métodos dedicados, hierarquia de erros, retry e hooks.
   Estas classes continuam funcionando com o mesmo contrato de antes
   (resposta ``(json_str, status_code)``, sem exceções tipadas).
"""
