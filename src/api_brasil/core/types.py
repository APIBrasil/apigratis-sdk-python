"""Tipos públicos da SDK: configuração, opções de requisição e envelopes."""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Literal, Optional, TypedDict, Union

__all__ = [
    "Json",
    "HttpMethod",
    "ResponseType",
    "RetryConfig",
    "HookRequestInfo",
    "HookResponseInfo",
    "HookRetryInfo",
    "ApiBrasilHooks",
    "ApiBrasilConfig",
    "RequestOptions",
    "DeviceServiceResponse",
    "CreditServiceResponse",
    "ConsultaPayload",
]

#: Corpo JSON já decodificado.
Json = Dict[str, Any]

HttpMethod = Literal["GET", "POST", "PUT", "PATCH", "DELETE"]

#: ``json`` (padrão), ``raw``/``bytes`` (binário), ``text`` ou ``stream``.
ResponseType = Literal["json", "raw", "bytes", "arraybuffer", "text", "stream"]


class RetryConfig(TypedDict, total=False):
    """Política de retry do cliente.

    Por padrão a SDK tenta novamente apenas em HTTP 429 (rate limit) e em
    falhas de conexão — nunca em timeouts ou erros de negócio, para não
    duplicar cobranças/envios.
    """

    #: Número de novas tentativas além da original. Padrão: 2.
    retries: int
    #: Atraso base do backoff exponencial em ms. Padrão: 300.
    min_delay_ms: int
    #: Teto do atraso entre tentativas em ms. Padrão: 5000.
    max_delay_ms: int
    #: Status HTTP que disparam retry. Padrão: ``[429]``.
    retry_on_statuses: List[int]


class HookRequestInfo(TypedDict):
    method: str
    url: str
    headers: Dict[str, str]
    body: Any
    #: Tentativa atual (0 = primeira).
    attempt: int


class HookResponseInfo(TypedDict):
    method: str
    url: str
    status: int
    duration_ms: int
    attempt: int


class HookRetryInfo(TypedDict):
    method: str
    url: str
    #: Número da próxima tentativa.
    attempt: int
    delay_ms: int
    reason: str


class ApiBrasilHooks(TypedDict, total=False):
    """Hooks de observabilidade — logging, métricas, tracing."""

    on_request: Callable[[HookRequestInfo], None]
    on_response: Callable[[HookResponseInfo], None]
    on_retry: Callable[[HookRetryInfo], None]


class ApiBrasilConfig(TypedDict, total=False):
    """Configuração do cliente :class:`~api_brasil.client.ApiBrasil`.

    Campos não informados são lidos das variáveis de ambiente
    ``APIBRASIL_BEARER_TOKEN``, ``APIBRASIL_DEVICE_TOKEN``,
    ``APIBRASIL_SECRET_KEY`` e ``APIBRASIL_BASE_URL``.
    """

    #: Token JWT obtido no login (``Authorization: Bearer <token>``).
    bearer_token: Optional[str]
    #: Token do dispositivo, exigido pelos serviços device-based.
    device_token: Optional[str]
    #: SecretKey da API (usada apenas na criação de devices).
    secret_key: Optional[str]
    #: Base da API. Padrão: ``https://gateway.apibrasil.io/api/v2``.
    base_url: Optional[str]
    #: Timeout das requisições em **milissegundos**. Padrão: 30000.
    timeout: Optional[int]
    #: Headers adicionais enviados em todas as requisições.
    headers: Optional[Dict[str, str]]
    #: Transporte HTTP customizado.
    transport: Optional[Any]
    #: Política de retry, ou ``False`` para desativar.
    retry: Union[RetryConfig, bool, None]
    #: Hooks de observabilidade.
    hooks: Optional[ApiBrasilHooks]


class RequestOptions(TypedDict, total=False):
    """Opções por requisição — sobrescrevem a configuração do cliente.

    Aceitas como ``**options`` no último parâmetro de qualquer método da SDK.
    """

    query: Dict[str, Any]
    headers: Dict[str, str]
    bearer_token: str
    device_token: str
    secret_key: str
    #: Timeout em milissegundos.
    timeout: int
    response_type: ResponseType


class DeviceServiceResponse(TypedDict, total=False):
    """Envelope de resposta dos serviços device-based."""

    error: bool
    message: str
    response: Any
    api_limit: Union[int, str]
    api_limit_for: str
    api_limit_used: Union[int, str]


class CreditServiceResponse(TypedDict, total=False):
    """Envelope de resposta das consultas por crédito."""

    error: bool
    message: str
    balance: Union[int, float, str]
    tax: Union[int, float, str]
    valor_consulta: Union[int, float, str]
    api_limit_for: str
    homolog: bool
    data: Any


class ConsultaPayload(TypedDict, total=False):
    """Campos comuns das consultas por crédito (``/consulta/{service}/credits``)."""

    #: Tipo/serviço da consulta (ex: ``serasa-score-pf``). Veja
    #: :data:`api_brasil.generated.catalog.CONSULTA_TIPOS`.
    tipo: str
    #: ``True`` ativa o modo homologação (sandbox, sem cobrança) quando suportado.
    homolog: bool
    #: Versão reduzida da consulta, quando suportada.
    lite: bool
    #: Consultas agrupadas.
    agrupados: List[str]
    #: Serviços extras.
    extra: List[str]
