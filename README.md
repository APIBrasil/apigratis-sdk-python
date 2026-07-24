# SDK Python - APIBrasil 🚀

SDK oficial Python da plataforma [APIBrasil](https://apibrasil.com.br) — WhatsApp, SMS, consultas de CPF/CNPJ, veículos, CEP, correios, pagamentos PIX/boleto e muito mais.

[![PyPI version](https://img.shields.io/pypi/v/api-brasil.svg)](https://pypi.org/project/api-brasil/)
[![Python versions](https://img.shields.io/pypi/pyversions/api-brasil.svg)](https://pypi.org/project/api-brasil/)
[![License MIT](https://img.shields.io/pypi/l/api-brasil.svg)](https://github.com/ivanildobarauna-dev/apibrasil-py/blob/main/LICENSE)

## Documentações das APIs

https://doc.apibrasil.io

## Deep Wiki

[![Ask to DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/ivanildobarauna-dev/apibrasil-py)

## Canais de suporte (Comunidade)

[![WhatsApp Group](https://img.shields.io/badge/WhatsApp-Group-25D366?logo=whatsapp)](https://chat.whatsapp.com/EeAWALQb6Ga5oeTbG7DD2k)
[![Telegram Group](https://img.shields.io/badge/Telegram-Group-32AFED?logo=telegram)](https://t.me/apigratisoficial)

## Instalação

```bash
pip install api-brasil
```

Ou com poetry:

```bash
poetry add api-brasil
```

Requer **Python >= 3.8**. Usa `requests` quando disponível e cai automaticamente
para a stdlib (`urllib`) — a camada de transporte é plugável.

Obtenha suas credenciais em https://apibrasil.com.br

## Começando

```python
import os
from api_brasil import ApiBrasil

api = ApiBrasil(
    bearer_token=os.environ["APIBRASIL_BEARER_TOKEN"],  # JWT do login
    device_token=os.environ["APIBRASIL_DEVICE_TOKEN"],  # device dos serviços device-based
)

# WhatsApp
api.whatsapp.send_text({"number": "5511999999999", "text": "Olá! 👋"})

# Consulta CNPJ (por créditos)
empresa = api.consulta.cnpj({"cnpj": "00000000000000"})
print(empresa["data"])
```

As credenciais também podem vir só do ambiente — `ApiBrasil()` lê automaticamente
`APIBRASIL_BEARER_TOKEN`, `APIBRASIL_DEVICE_TOKEN`, `APIBRASIL_SECRET_KEY` e `APIBRASIL_BASE_URL`.

Todas as respostas são devolvidas como **dicionário** já decodificado.

Também é possível autenticar por email/senha — o token retornado fica guardado no cliente:

```python
api = ApiBrasil()
api.auth.login({"email": "voce@empresa.com.br", "password": "******"})

# contas com 2FA:
session = api.auth.login({"email": email, "password": password})
if session.get("requires_2fa"):
    api.auth.send_2fa({"challenge": session["challenge"], "method": "email"})
    api.auth.verify_2fa({"challenge": session["challenge"], "code": "000000"})
```

## Como a plataforma funciona

A API Brasil tem duas famílias de serviços:

| Família          | Autenticação                                   | Exemplos                                                                    |
| ---------------- | ---------------------------------------------- | --------------------------------------------------------------------------- |
| **Device-based** | `Authorization: Bearer` + header `DeviceToken` | WhatsApp, SMS, veículos, CEP, correios, DDD, feriados, tradução, clima, OCR |
| **Por créditos** | apenas `Authorization: Bearer` (debita saldo)  | `consulta.cpf`, `consulta.cnpj`, `consulta.veiculos`, Serasa, CNH, telefone |

Para os serviços device-based, crie um device com a `SecretKey` da API desejada (painel APIBrasil) e use o `device_token` retornado:

```python
device = api.devices.store(
    {"device_name": "meu-bot", "type": "server"},
    secret_key="SUA_SECRET_KEY",
)

api.set_device_token(device["device"]["device_token"])
```

## Serviços disponíveis

| Módulo                                                  | Descrição                                                                                              |
| ------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| `api.whatsapp`                                          | WhatsApp: `start`, `qrcode`, `send_text`, `send_file`, `send_audio`, `send_video`, fila (`queue`)...  |
| `api.evolution`                                         | Evolution API: `request(controller, action, body)`                                                    |
| `api.whatsmeow`                                         | WhatsMeow: `request(action, body)`                                                                    |
| `api.sms`                                               | SMS device-based (`send`) e por créditos (`send_with_credits`)                                        |
| `api.dados`                                             | Dados cadastrais device-based (`cpf`, `cnpj`)                                                          |
| `api.vehicles`                                          | Veículos por placa (`dados`, `fipe`, `consulta_fipe`)                                                  |
| `api.fipe`                                              | Tabela FIPE (`request(action, body)`)                                                                 |
| `api.correios`                                          | Correios (`rastreio`, `request`)                                                                       |
| `api.cep`                                               | CEP + geolocalização (`cep`, `request`)                                                                |
| `api.geolocation` / `api.geomatrix`                     | Geolocalização e matriz de distâncias                                                                  |
| `api.recognize`                                         | OCR / Google Vision                                                                                    |
| `api.ddd` / `api.holidays` / `api.translate` / `api.weather` | DDD, feriados, tradução, clima                                                                    |
| `api.database_ip`                                       | GeoIP (`ip`)                                                                                           |
| `api.consulta`                                          | Consultas por créditos: `cpf`, `cnpj`, `cnh`, `cep`, `veiculos`, `telefone`, `generic(service, body)` |
| `api.ura` / `api.chip_virtual`                          | URA reversa e chip virtual                                                                             |
| `api.bulk`                                              | Execução em lote (`direct`, `queue`)                                                                   |
| `api.auth`                                              | Login, 2FA, cadastro, recuperação de senha, perfil                                                     |
| `api.devices`                                           | CRUD de devices                                                                                        |
| `api.catalog`                                           | Catálogo de APIs, planos, documentações, servidores                                                    |
| `api.account`                                           | Saldo, faturas, notificações, tickets                                                                  |
| `api.payments`                                          | Recargas e pagamentos PIX/boleto/cartão (Santander, Inter, Mercado Pago, Sicoob)                       |
| `api.ip_whitelist` / `api.bearer_rate_limit`            | Segurança da conta                                                                                     |
| `api.reports`                                           | Relatórios e dashboard de consumo                                                                      |

### WhatsApp

```python
# iniciar sessão e obter QR Code
api.whatsapp.start({"webhook_wh_message": "https://seu-webhook.com/mensagens"})

qr = api.whatsapp.qrcode()
print(qr["response"]["qrcode"])  # data URI base64

# envios
api.whatsapp.send_text({"number": "5511999999999", "text": "Olá!"})
api.whatsapp.send_file({"number": "5511999999999", "path": "https://exemplo.com/nota.pdf"})
api.whatsapp.send_audio({"number": "5511999999999", "path": "https://exemplo.com/audio.mp3"})

# qualquer action da documentação, inclusive via fila
api.whatsapp.request("sendLocation", {"number": "5511999999999", "lat": -23.5, "lng": -46.6})
api.whatsapp.queue("sendText", {"number": "5511999999999", "text": "assíncrono 🚀"})
```

### Consultas por créditos

```python
# CPF / CNPJ
cpf = api.consulta.cpf({"cpf": "00000000000"})
socios = api.consulta.cnpj({"cnpj": "00000000000000", "tipo": "lista-socios"})

# veicular
veiculo = api.consulta.veiculos({"placa": "ABC1234"})

# qualquer produto do catálogo
score = api.consulta.generic("cpf", {"cpf": "00000000000", "tipo": "serasa-score-pf"})

# homologação (sandbox, sem cobrança)
teste = api.consulta.cpf({"cpf": "00000000000", "homolog": True})
```

### Veículos e FIPE (device-based)

```python
dados = api.vehicles.dados({"placa": "ABC1234"})
fipe = api.vehicles.fipe({"placa": "ABC1234"})
```

### SMS

```python
api.sms.send({"number": "5511999999999", "message": "Seu código: 123456"})
# ou debitando créditos da conta (sem device):
api.sms.send_with_credits({"number": "5511999999999", "message": "Olá!"})
```

### Pagamentos e recargas

```python
pix = api.payments.pix_generate("inter", {"amount": 100})
status = api.payments.pix_status("inter", pix["txId"])

boleto = api.payments.boleto_generate("sicoob", {"amount": 150})
pdf = api.payments.boleto_pdf("sicoob", boleto["id"])  # conteúdo binário (bytes)
```

### Múltiplos devices

```python
comercial = api.with_device("DEVICE_TOKEN_COMERCIAL")
suporte = api.with_device("DEVICE_TOKEN_SUPORTE")

comercial.whatsapp.send_text({"number": "55...", "text": "Proposta enviada!"})
suporte.whatsapp.send_text({"number": "55...", "text": "Como posso ajudar?"})
```

## Tratamento de erros

Cada categoria de falha tem a sua própria classe — todas estendem `ApiBrasilError`
(que por sua vez estende `Exception`):

| Classe                          | Quando                                     |
| ------------------------------- | ------------------------------------------ |
| `ValidationError`               | 400/422 — payload inválido                 |
| `AuthenticationError`           | 401 — token ausente/expirado               |
| `InsufficientBalanceError`      | 402 — sem saldo/créditos                   |
| `PermissionError`               | 403 — sem permissão (ex: exige PJ)         |
| `NotFoundError`                 | 404/410 — sem dados / rota desativada      |
| `RateLimitError`                | 429 — limite atingido (`retry_after_ms`)   |
| `ServerError`                   | 5xx — erro do gateway/provedor             |
| `NetworkError` / `TimeoutError` | falha antes da resposta                    |

```python
from api_brasil import InsufficientBalanceError, RateLimitError

try:
    api.consulta.cpf({"cpf": "00000000000"})
except InsufficientBalanceError:
    print("Recarregue seus créditos")
except RateLimitError as e:
    print(f"Aguarde {e.retry_after_ms}ms")
```

Todo erro expõe `status` (HTTP), `code` (código da API) e `response` (corpo completo da resposta).

> **Nota:** `PermissionError` e `TimeoutError` têm o mesmo nome de builtins do Python.
> Se precisar evitar o sombreamento no seu módulo, importe os aliases
> `ApiBrasilPermissionError` e `ApiBrasilTimeoutError`.

## Retry e observabilidade

Por padrão a SDK refaz a chamada em **HTTP 429** e em **falhas de conexão** (2 tentativas extras, backoff exponencial, respeitando `Retry-After`). Timeouts e erros de negócio nunca são refeitos — evita duplicar cobranças e envios.

```python
api = ApiBrasil(
    retry={"retries": 3, "min_delay_ms": 500, "retry_on_statuses": [429, 503]},  # ou retry=False
    hooks={
        "on_request": lambda i: print(f"→ {i['method']} {i['url']} (#{i['attempt']})"),
        "on_response": lambda i: print(f"← {i['status']} em {i['duration_ms']}ms"),
        "on_retry": lambda i: print(f"retry em {i['delay_ms']}ms: {i['reason']}"),
    },
)
```

## Transporte plugável

O HTTP é feito pelo `requests` (com fallback para a stdlib), mas a interface `Transport`
permite trocar a camada inteira (proxy corporativo, outro cliente, mocks de teste):

```python
import requests
from api_brasil import ApiBrasil, RequestsTransport

# requests com uma Session própria (proxy, verify, retries de conexão...)
session = requests.Session()
session.proxies = {"https": "http://proxy.local:3128"}

api = ApiBrasil(transport=RequestsTransport(session=session))
```

Ou implemente a sua:

```python
from api_brasil import Transport, TransportRequest, TransportResponse

class MeuTransporte(Transport):
    def request(self, request: TransportRequest) -> TransportResponse:
        # use o cliente HTTP que quiser e devolva status, headers e corpo
        return TransportResponse(200, {}, {"ok": True})

api = ApiBrasil(transport=MeuTransporte())
```

## Catálogo gerado

As actions de WhatsApp/Evolution/WhatsMeow e os 210+ `tipo` de consulta estão
disponíveis em constantes geradas do catálogo real da plataforma
(`python scripts/codegen.py` atualiza):

```python
from api_brasil import catalog

catalog.WHATSAPP_ACTIONS                 # ['sendText', 'sendFile', ...]
catalog.service_actions("whatsmeow")     # actions documentadas do serviço
catalog.consulta_tipo("lista-socios")    # {'service': 'cnpj', 'fields': ['cnpj']}
```

## Endpoint sem método dedicado?

Todo o gateway fica acessível pela porta de saída genérica, já com seus headers de autenticação:

```python
api.request("POST", "/consulta/cpf/credits", {"cpf": "00000000000"})
api.request("GET", "/reports/quick-stats")
```

Documentação completa dos endpoints: https://doc.apibrasil.io

## Configuração avançada

```python
api = ApiBrasil(
    bearer_token="...",  # ou APIBRASIL_BEARER_TOKEN
    device_token="...",  # ou APIBRASIL_DEVICE_TOKEN
    secret_key="...",    # usada em devices.store (ou APIBRASIL_SECRET_KEY)
    base_url="https://gateway.apibrasil.io/api/v2",  # padrão (ou APIBRASIL_BASE_URL)
    timeout=30000,       # milissegundos
    headers={"X-Custom": "valor"},  # headers extras
    retry={"retries": 2},           # ou False
    hooks={"on_retry": lambda i: print(i["reason"])},
    transport=None,      # Transport customizado
)
```

Opções por requisição (`**options` no último parâmetro de qualquer método): `query`,
`headers`, `bearer_token`, `device_token`, `secret_key`, `timeout`, `response_type`.

```python
api.whatsapp.send_text(
    {"number": "5511999999999", "text": "Olá!"},
    device_token="OUTRO_DEVICE",
    timeout=60000,
)
```

> **Atenção:** `timeout` é em **milissegundos** (igual às SDKs Node/PHP).

## Interface legada (`APIBrasilClient` + `WhatsAppApi`, ...)

A interface antiga continua funcionando exatamente como antes (resposta
`(json_str, status_code)`, sem exceções tipadas), mas está **deprecada** — prefira
o cliente `ApiBrasil`.

<details>
<summary>Exemplos da interface legada</summary>

### WhatsAppApi

```python
from api_brasil import APIBrasilClient, WhatsAppApi

api_brasil_client = APIBrasilClient(bearer_token="your_bearer_token_here")

whatsapp_api = WhatsAppApi(api_brasil_client=api_brasil_client, device_token="your_device_token_here")
whatsapp_api.to_number(phone_number="5511999999999")
response, status_code = whatsapp_api.send_message(message="Hello, API Brasil!")
print(response, status_code)
```

### VehiclesApi

```python
from api_brasil import APIBrasilClient, VehiclesApi
from api_brasil.features.vehicles import Endpoints

api_brasil_client = APIBrasilClient(bearer_token="your_bearer_token_here")

vehicles_api = VehiclesApi(api_brasil_client=api_brasil_client, device_token="your_device_token_here")
vehicles_api.set_plate(plate="ABC-1234")
response, status_code = vehicles_api.consulta(vechiles_api_endpoint=Endpoints.dados)
print(response, status_code)
```

### CNPJApi / CPFApi

```python
from api_brasil import APIBrasilClient, CNPJApi, CPFApi

api_brasil_client = APIBrasilClient(bearer_token="your_bearer_token_here")

cnpj_api = CNPJApi(api_brasil_client=api_brasil_client, device_token="your_device_token")
cnpj_api.set_cnpj(cnpj="44.959.669/0001-80")
print(cnpj_api.consulta())

cpf_api = CPFApi(api_brasil_client=api_brasil_client, device_token="your_device_token")
cpf_api.set_cpf(cpf="00000000000")
print(cpf_api.consulta())
```

### CorreiosAPI / CEPGeoLocationAPI / SMSApi

```python
from api_brasil import APIBrasilClient, CorreiosAPI, CEPGeoLocationAPI, SMSApi

api_brasil_client = APIBrasilClient(bearer_token="your_bearer_token_here")

correios_api = CorreiosAPI(api_brasil_client=api_brasil_client, device_token="your_device_token")
correios_api.set_track_code(track_code="PN123456789BR")
print(correios_api.track())

cep_api = CEPGeoLocationAPI(api_brasil_client=api_brasil_client, device_token="your_device_token")
cep_api.set_cep(cep="00000-000")
print(cep_api.consulta())

sms = SMSApi(api_brasil_client=api_brasil_client, device_token="your_device_token")
sms.set_phone_number(number="5511900000000")
print(sms.send(message="Hello, API Brasil!"))
```

</details>

## Mais informações

https://pypi.org/project/api-brasil/
