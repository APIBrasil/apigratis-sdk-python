"""Serviços da SDK, organizados por domínio."""

from .data import (
    BulkService,
    CepService,
    ChipVirtualService,
    ConsultaService,
    CorreiosService,
    DadosService,
    DatabaseIpService,
    FipeService,
    UraService,
    VehiclesService,
)
from .device_proxy import DeviceProxyService
from .messaging import (
    EvolutionService,
    SmsService,
    WhatsAppService,
    WhatsMeowService,
)
from .platform import (
    AccountService,
    AuthService,
    BearerRateLimitService,
    CatalogService,
    DevicesService,
    IpWhitelistService,
    PaymentsService,
    ReportsService,
)

__all__ = [
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
]
