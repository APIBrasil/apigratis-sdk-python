# Changelog

## 2.0.1 — 2026-07-24

Novo cliente `ApiBrasil` cobrindo toda a plataforma APIBrasil — mesma
arquitetura, mesmos endpoints e mesmas funções das SDKs Node.js, PHP e Flutter.
Release totalmente retrocompatível: nada da interface antiga foi alterado.

### Novidades

- **Cliente central `api_brasil.ApiBrasil`** com módulos por produto: `whatsapp`, `evolution`, `whatsmeow`, `sms`, `dados`, `vehicles`, `fipe`, `correios`, `cep`, `geolocation`, `geomatrix`, `recognize`, `ddd`, `holidays`, `translate`, `weather`, `loterias`, `database_ip`, `consulta` (créditos), `ura`, `chip_virtual`, `bulk`, `auth` (login/2FA), `devices`, `catalog`, `account`, `payments` (PIX/boleto/cartão), `ip_whitelist`, `bearer_rate_limit`, `reports`.
- **Transporte plugável** (`Transport`): `RequestsTransport` por padrão, `UrllibTransport` sem dependências como fallback, e injeção de implementações próprias para proxies e mocks.
- **Retry com backoff exponencial** (padrão: HTTP 429 e falhas de conexão; nunca timeouts nem erros de negócio) com suporte a `Retry-After`.
- **Hooks de observabilidade**: `on_request`, `on_response`, `on_retry`.
- **Hierarquia de erros**: `ValidationError`, `AuthenticationError`, `InsufficientBalanceError`, `PermissionError`, `NotFoundError`, `RateLimitError`, `ServerError`, `NetworkError`, `TimeoutError` — todas estendendo `ApiBrasilError`.
- **Variáveis de ambiente**: `APIBRASIL_BEARER_TOKEN`, `APIBRASIL_DEVICE_TOKEN`, `APIBRASIL_SECRET_KEY`, `APIBRASIL_BASE_URL` lidas automaticamente.
- **Catálogo gerado** (`python scripts/codegen.py`): `catalog.WHATSAPP_ACTIONS`, `EVOLUTION_PATHS`, `WHATSMEOW_ACTIONS`, `CONSULTA_SERVICOS`, `CONSULTA_TIPOS` (210+ tipos) e `SERVICE_ACTIONS`.
- **Testes** unitários com transporte fake (296 casos, cobrindo todas as rotas e todo o catálogo — sem rede) e marcador `py.typed` (PEP 561).

### Compatibilidade

- A interface legada (`APIBrasilClient` + `WhatsAppApi`, `CNPJApi`, `CPFApi`, `CorreiosAPI`, `CEPGeoLocationAPI`, `SMSApi`, `VehiclesApi`) continua funcionando com o **mesmo contrato**: mesmos métodos, mesma resposta `(json_str, status_code)`, sem exceções tipadas. Está marcada como deprecated — prefira `ApiBrasil(...)`.

### Notas

- No cliente novo, `timeout` é em **milissegundos** (paridade com as SDKs Node/PHP). As respostas são **dicionários** já decodificados.
- Compatível com **Python 3.8+**.

## 2.0.0

Interface por feature (`APIBrasilClient` + `WhatsAppApi`, `CNPJApi`,
`CPFApi`, `CorreiosAPI`, `CEPGeoLocationAPI`, `SMSApi`, `VehiclesApi`).
