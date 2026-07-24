"""Cliente oficial da plataforma APIBrasil."""

from __future__ import annotations

from typing import Any, Mapping, NamedTuple, Optional

from .core.errors import ApiBrasilError
from .core.http import HttpClient
from .core.types import Json
from .services.data import (
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
from .services.device_proxy import DeviceProxyService
from .services.messaging import (
    EvolutionService,
    SmsService,
    WhatsAppService,
    WhatsMeowService,
)
from .services.platform import (
    AccountService,
    AuthService,
    BearerRateLimitService,
    CatalogService,
    DevicesService,
    IpWhitelistService,
    PaymentsService,
    ReportsService,
)

__all__ = ["ApiBrasil", "LoginResult"]


class LoginResult(NamedTuple):
    """Retorno de :meth:`ApiBrasil.login`."""

    client: "ApiBrasil"
    session: Any


class ApiBrasil:
    """Cliente oficial da plataforma APIBrasil.

    .. code-block:: python

        from api_brasil import ApiBrasil

        api = ApiBrasil(
            bearer_token=os.environ["APIBRASIL_BEARER_TOKEN"],
            device_token=os.environ["APIBRASIL_DEVICE_TOKEN"],
        )

        api.whatsapp.send_text({"number": "5511999999999", "text": "Olá!"})
        cnpj = api.consulta.cnpj({"cnpj": "00000000000000"})

    Credenciais não informadas são lidas das variáveis de ambiente
    ``APIBRASIL_BEARER_TOKEN``, ``APIBRASIL_DEVICE_TOKEN``,
    ``APIBRASIL_SECRET_KEY`` e ``APIBRASIL_BASE_URL``.
    """

    def __init__(
        self, config: Optional[Mapping[str, Any]] = None, **overrides: Any
    ) -> None:
        #: Cliente HTTP interno (headers, base URL, retry, hooks, erros).
        self.http = HttpClient(config, **overrides)

        #: Login, 2FA, cadastro, senha e perfil.
        self.auth = AuthService(self.http)
        #: Gestão de devices (criar, listar, atualizar, remover).
        self.devices = DevicesService(self.http)

        #: WhatsApp device-based (``/whatsapp/{action}``).
        self.whatsapp = WhatsAppService(self.http)
        #: Evolution API (``/evolution/{controller}/{action}``).
        self.evolution = EvolutionService(self.http)
        #: WhatsMeow (``/whatsmeow/{action}``).
        self.whatsmeow = WhatsMeowService(self.http)
        #: SMS (``/sms/{action}`` e ``/sms/send/credits``).
        self.sms = SmsService(self.http)

        #: Dados cadastrais device-based (``/dados/cpf``, ``/dados/cnpj``...).
        self.dados = DadosService(self.http)
        #: Veículos por placa (``/vehicles/dados``, ``/vehicles/fipe``).
        self.vehicles = VehiclesService(self.http)
        #: Tabela FIPE (``/fipe/{action}``).
        self.fipe = FipeService(self.http)
        #: Correios (``/correios/{action}``).
        self.correios = CorreiosService(self.http)
        #: CEP + geolocalização (``/cep/{action}``).
        self.cep = CepService(self.http)
        #: Geolocalização (``/geolocation/{action}``).
        self.geolocation = DeviceProxyService(self.http, "geolocation")
        #: Matriz de distâncias (``/geomatrix/{action}``).
        self.geomatrix = DeviceProxyService(self.http, "geomatrix")
        #: OCR / Google Vision (``/recognize/{action}``).
        self.recognize = DeviceProxyService(self.http, "recognize")
        #: DDD (``/ddd/{action}``).
        self.ddd = DeviceProxyService(self.http, "ddd")
        #: Feriados (``/holidays/{action}``).
        self.holidays = DeviceProxyService(self.http, "holidays")
        #: Tradução (``/translate/{action}``).
        self.translate = DeviceProxyService(self.http, "translate")
        #: Clima (``/weather/{action}``).
        self.weather = DeviceProxyService(self.http, "weather")
        #: Loterias (``/loterias/{action}``).
        self.loterias = DeviceProxyService(self.http, "loterias")
        #: GeoIP (``/database/ip``).
        self.database_ip = DatabaseIpService(self.http)

        #: Consultas por crédito (``/consulta/{servico}/credits``).
        self.consulta = ConsultaService(self.http)
        #: URA reversa / ligações (``/ura/call/*``).
        self.ura = UraService(self.http)
        #: Chip virtual (``/chip/virtual/*``).
        self.chip_virtual = ChipVirtualService(self.http)
        #: Execução em lote (``/bulk/*``).
        self.bulk = BulkService(self.http)

        #: Catálogo de APIs, planos, docs e servidores.
        self.catalog = CatalogService(self.http)
        #: Saldo, faturas, notificações, tickets.
        self.account = AccountService(self.http)
        #: Recargas e pagamentos (PIX, boleto, cartão).
        self.payments = PaymentsService(self.http)
        #: IP whitelist da conta.
        self.ip_whitelist = IpWhitelistService(self.http)
        #: Rate limit por Bearer Token.
        self.bearer_rate_limit = BearerRateLimitService(self.http)
        #: Relatórios e dashboard de consumo.
        self.reports = ReportsService(self.http)

    @classmethod
    def login(
        cls,
        credentials: Json,
        config: Optional[Mapping[str, Any]] = None,
        **overrides: Any,
    ) -> LoginResult:
        """Faz login e retorna um cliente já autenticado.

        Lança :class:`~api_brasil.core.errors.ApiBrasilError` se a conta exigir
        2FA — nesse caso crie o cliente manualmente e use ``auth.login()`` +
        ``auth.verify_2fa()``.

        :param credentials: ``email`` e ``password``
        :return: ``(client, session)``
        """
        client = cls(config, **overrides)
        session = client.auth.login(credentials)

        if isinstance(session, Mapping) and session.get("requires_2fa"):
            raise ApiBrasilError(
                "Esta conta exige autenticação em dois fatores. "
                "Use auth.login() + auth.verify_2fa().",
                response=session,
            )

        return LoginResult(client, session)

    def set_bearer_token(self, token: str) -> "ApiBrasil":
        """Define/atualiza o Bearer Token do cliente."""
        self.http.set_bearer_token(token)

        return self

    def set_device_token(self, token: str) -> "ApiBrasil":
        """Define/atualiza o DeviceToken do cliente."""
        self.http.set_device_token(token)

        return self

    def with_device(self, device_token: str) -> "ApiBrasil":
        """Novo cliente com as mesmas credenciais, apontando para outro device.

        Útil para gerenciar vários números/instâncias.
        """
        config = self.http.get_config()
        config["device_token"] = device_token

        return ApiBrasil(config)

    def request(
        self,
        method: str,
        path: str,
        body: Any = None,
        **options: Any,
    ) -> Any:
        """Porta de saída genérica: chama qualquer endpoint do gateway.

        Já com os headers de autenticação configurados. Use para rotas que
        ainda não têm método dedicado na SDK.

        .. code-block:: python

            api.request("POST", "/consulta/cpf/credits", {"cpf": "..."})
            api.request("GET", "/reports/quick-stats")
        """
        return self.http.request(method, path, body, **options)
