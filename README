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
| O | WhatsAppService                | API do WhatsApp Gratuita.               |   O   | O                   | x                   |
| x | Receita Data CNPJ              | API Dados CNPJ Receita.                 |   x   | x                   | x                   |
| x | Receita Data CPF               | API Dados de CPF Serasa.                |   x   | x                   | x                   |
| x | CorreiosService                | API Busca encomendas Correios Brazil.   |   x   | x                   | x                   |
| x | CEPLocation                    | API CEP Geolocation + IBGE Brazil.      |   x   | x                   | x                   |
| x | VehiclesService                | API Placa Dados.                        |   x   | x                   | x                   |
| x | FipeService                    | API Placa FIPE.                         |   x   | x                   | x                   |

## Como utilizar

_Voce pode utilizar todos os endpoints da API do WhatsApp, basta mudar o action e o body_

## Documentacoes
https://apibrasil.com.br/documentacoes


```python

from apigratis.Service import Service
import json

def main():

    sendText = Service.whatsapp(json.dumps({
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
    main()
```
