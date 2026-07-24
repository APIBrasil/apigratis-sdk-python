"""Serviços de dados e consultas."""

from .bulk import BulkService
from .cep import CepService
from .chip_virtual import ChipVirtualService
from .consulta import ConsultaService
from .correios import CorreiosService
from .dados import DadosService
from .database_ip import DatabaseIpService
from .fipe import FipeService
from .ura import UraService
from .vehicles import VehiclesService

__all__ = [
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
]
