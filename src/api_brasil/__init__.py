"""SDK oficial Python da plataforma APIBrasil.

WhatsApp, SMS, consultas de CPF/CNPJ, veículos, CEP, correios, pagamentos
PIX/boleto e muito mais — https://apibrasil.com.br

.. code-block:: python

    from api_brasil import ApiBrasil

    api = ApiBrasil(bearer_token="...", device_token="...")
    api.whatsapp.send_text({"number": "5511999999999", "text": "Olá!"})

A interface antiga (``APIBrasilClient`` + ``WhatsAppApi``, ``CNPJApi``, ...)
continua funcionando, mas está **deprecada** — prefira ``ApiBrasil``.
"""

# Cliente principal
from .client import ApiBrasil, LoginResult

# Núcleo: HTTP, transporte, erros, retry, ambiente e tipos
from .core import (
    DEFAULT_BASE_URL,
    DEFAULT_RETRY,
    DEFAULT_TIMEOUT,
    ENV_VARS,
    SDK_USER_AGENT,
    ApiBrasilConfig,
    ApiBrasilError,
    ApiBrasilHooks,
    ApiBrasilPermissionError,
    ApiBrasilTimeoutError,
    AuthenticationError,
    ConsultaPayload,
    CreditServiceResponse,
    DeviceServiceResponse,
    HttpClient,
    InsufficientBalanceError,
    Json,
    NetworkError,
    NotFoundError,
    PermissionError,
    RateLimitError,
    RequestOptions,
    RequestsTransport,
    RetryConfig,
    ServerError,
    TimeoutError,
    Transport,
    TransportRequest,
    TransportResponse,
    UrllibTransport,
    ValidationError,
    config_from_env,
    create_api_error,
)

# Catálogo gerado do gateway
from .generated import catalog

# Serviços por domínio
from .services import (
    AccountService,
    AuthService,
    BearerRateLimitService,
    BulkService,
    CatalogService,
    CepService,
    ChipVirtualService,
    ConsultaService,
    CorreiosService,
    DadosService,
    DatabaseIpService,
    DeviceProxyService,
    DevicesService,
    EvolutionService,
    FipeService,
    IpWhitelistService,
    PaymentsService,
    ReportsService,
    SmsService,
    UraService,
    VehiclesService,
    WhatsAppService,
    WhatsMeowService,
)

# --------------------------------------------------------------------------
# Interface legada (<= 2.0.x) — mantida por compatibilidade.
# `api_client` precisa ser importado antes de `features`, que depende dele.
# --------------------------------------------------------------------------
from .api_client.client_builder import APIBrasilClient
from .features.cep_geolocation import CEPGeoLocationAPI
from .features.cnpj import CNPJApi
from .features.correios import CorreiosAPI
from .features.cpf import CPFApi
from .features.sms import SMSApi
from .features.vehicles import VehiclesApi
from .features.whatsapp import WhatsAppApi

__version__ = "2.0.1"

__all__ = [
    "__version__",
    # Cliente
    "ApiBrasil",
    "LoginResult",
    # Núcleo
    "HttpClient",
    "DEFAULT_BASE_URL",
    "DEFAULT_TIMEOUT",
    "SDK_USER_AGENT",
    "DEFAULT_RETRY",
    "ENV_VARS",
    "config_from_env",
    "Transport",
    "TransportRequest",
    "TransportResponse",
    "RequestsTransport",
    "UrllibTransport",
    "ApiBrasilError",
    "NetworkError",
    "TimeoutError",
    "ValidationError",
    "AuthenticationError",
    "InsufficientBalanceError",
    "PermissionError",
    "NotFoundError",
    "RateLimitError",
    "ServerError",
    "ApiBrasilPermissionError",
    "ApiBrasilTimeoutError",
    "create_api_error",
    "ApiBrasilConfig",
    "ApiBrasilHooks",
    "RequestOptions",
    "RetryConfig",
    "ConsultaPayload",
    "CreditServiceResponse",
    "DeviceServiceResponse",
    "Json",
    # Catálogo
    "catalog",
    # Serviços
    "DeviceProxyService",
    "WhatsAppService",
    "EvolutionService",
    "WhatsMeowService",
    "SmsService",
    "BulkService",
    "CepService",
    "ChipVirtualService",
    "ConsultaService",
    "CorreiosService",
    "DadosService",
    "DatabaseIpService",
    "FipeService",
    "UraService",
    "VehiclesService",
    "AccountService",
    "AuthService",
    "BearerRateLimitService",
    "CatalogService",
    "DevicesService",
    "IpWhitelistService",
    "PaymentsService",
    "ReportsService",
    # Legado
    "APIBrasilClient",
    "WhatsAppApi",
    "VehiclesApi",
    "CNPJApi",
    "CPFApi",
    "CorreiosAPI",
    "CEPGeoLocationAPI",
    "SMSApi",
]
