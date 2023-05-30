# SDK Python - APIGratis by API BRASIL 🚀

Conjunto de API, para desenvolvedores.

_Transforme seus projetos em soluções inteligentes com nossa API. Com recursos como API do WhatsApp, geolocalização, rastreamento de encomendas, verificação de CPF/CNPJ e mais, você pode criar soluções eficientes e funcionais. Comece agora._

## Como instalar

```pip3 install apigratis==0.0.3```
## Canais de suporte (Comunidade)
[![WhatsApp Group](https://img.shields.io/badge/WhatsApp-Group-25D366?logo=whatsapp)](https://chat.whatsapp.com/KsxrUGIPWvUBYAjI1ogaGs)
[![Telegram Group](https://img.shields.io/badge/Telegram-Group-32AFED?logo=telegram)](https://t.me/apigratisoficial)

## Obtenha suas credenciais
https://apigratis.com.br

## Mais informações

https://pypi.org/project/apigratis/0.1.0/

## Serviços de API disponíveis

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

```python

from apigratis.Service import Service
import json

def main():

    sendText = Service.whatsapp(json.dumps({
        "action": "sendText",
        "credentials": {
            "SecretKey": "SEU_SECRET_KEY"
            "PublicToken": "SEU_PUBLIC_TOKEN",
            "DeviceToken": "SEU_DEVICE_TOKEN",
            "BearerToken": "SEU_BEARER_TOKEN",
        },
        "body": {
            "message": "Hello World por Python",
            "phone": "5531994359434",
            "time_typing": 1
        }
    }))

    print(sendText)

if __name__ == "__main__":
    main()
```