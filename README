# SDK Python - APIGratis by API BRASIL

Conjunto de API, para desenvolvedores.

_Transforme seus projetos em solucoes inteligentes com nossa API. Com recursos como API do WhatsApp, geolocalizacao, rastreamento de encomendas, verificacao de CPF/CNPJ e mais, voce pode criar solucoes eficientes e funcionais._

## Como instalar

```pip install apigratis-sdk-python```
## Canais de suporte (Comunidade)
[![WhatsApp Group](https://img.shields.io/badge/WhatsApp-Group-25D366?logo=whatsapp)](https://chat.whatsapp.com/KsxrUGIPWvUBYAjI1ogaGs)
[![Telegram Group](https://img.shields.io/badge/Telegram-Group-32AFED?logo=telegram)](https://t.me/apigratisoficial)

## Obtenha suas credenciais
https://apigratis.com.br

## Mais informacoes

https://pypi.org/project/apigratis-sdk-python

## Servicos de API disponiveis

| Up  | Services available            | Description       | Free    | Beta        | Stable   |
------|-------------------------------|-------------------|---------| ------------------------- | ------------------------- |
| ✓ | WhatsAppService                | API do WhatsApp Gratuita.               |   ✓   | ✓                   | x                   |
| ✓ | Receita Data CNPJ              | API Dados CNPJ Receita.                 |   ✓   | ✓                   | x                   |
| ✓ | Receita Data CPF               | API Dados de CPF Serasa.                |   ✓   | ✓                   | x                   |
| ✓ | CorreiosService                | API Busca encomendas Correios Brazil.   |   ✓   | ✓                   | x                   |
| ✓ | CEPLocation                    | API CEP Geolocation + IBGE Brazil.      |   ✓   | ✓                   | x                   |
| ✓ | VehiclesService                | API Placa Dados.                        |   ✓   | ✓                   | x                   |
| ✓ | FipeService                    | API Placa FIPE.                         |   ✓   | ✓                   | x                   |

## Como utilizar

_Voce pode utilizar todos os endpoints da API do WhatsApp, basta mudar o action e o body_

## Documentacoes
https://apibrasil.com.br/documentacoes

## WhatsApp Service

```python
from apigratis.Service import Service
import json

def whatsapp():

    sendText = Service().whatsapp(json.dumps({
        "action": "sendText",
        "credentials": {
            "SecretKey": "SEU_SECRET_KEY",
            "PublicToken": "SEU_PUBLIC_TOKEN",
            "DeviceToken": "SEU_DEVICE_TOKEN",
            "BearerToken": "SEU_BEARER_TOKEN",
        },
        "body": {
            "message": "Hello World for Python",
            "phone": "5531994359434",
            "time_typing": 1
        }
    }))

    print(sendText)

if __name__ == "__main__":
    whatsapp()
```

## Vehicles Data Service

```python
from apigratis.Service import Service
import json

def vehicles():

    vehicle = Service().vehicles(json.dumps({
        "action": "dados",
        "credentials": {
            "SecretKey": "SEU_SECRET_KEY",
            "PublicToken": "SEU_PUBLIC_TOKEN",
            "DeviceToken": "SEU_DEVICE_TOKEN",
            "BearerToken": "SEU_BEARER_TOKEN",
        },
        "body": {
            "placa": "OQH3065",
        }
    }))

    print(vehicle)

if __name__ == "__main__":
    vehicles()
```

## Vehicles FIPE Service

```python
from apigratis.Service import Service
import json

def fipe():

    vehicle = Service().vehicles(json.dumps({
        "action": "fipe",
        "credentials": {
            "SecretKey": "SEU_SECRET_KEY",
            "PublicToken": "SEU_PUBLIC_TOKEN",
            "DeviceToken": "SEU_DEVICE_TOKEN",
            "BearerToken": "SEU_BEARER_TOKEN",
        },
        "body": {
            "placa": "OQH3065",
        }
    }))

    print(vehicle)

if __name__ == "__main__":
    fipe()
```

## CNPJ

```python
from apigratis.Service import Service
import json

def fipe():

    vehicle = Service().vehicles(json.dumps({
        "action": "/",
        "credentials": {
            "SecretKey": "SEU_SECRET_KEY",
            "PublicToken": "SEU_PUBLIC_TOKEN",
            "DeviceToken": "SEU_DEVICE_TOKEN",
            "BearerToken": "SEU_BEARER_TOKEN",
        },
        "body": {
            "placa": "OQH3065",
        }
    }))

    print(vehicle)

if __name__ == "__main__":
    fipe()
```