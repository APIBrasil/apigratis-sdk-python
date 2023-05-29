# SDK Python - APIGratis by API BRASIL 🚀

Conjunto de API, para desenvolvedores.

_Transforme seus projetos em soluções inteligentes com nossa API. Com recursos como API do WhatsApp, geolocalização, rastreamento de encomendas, verificação de CPF/CNPJ e mais, você pode criar soluções eficientes e funcionais. Comece agora._

#Como instalar

```pip3 install apigratis==0.0.9```
## Canais de suporte (Comunidade)
[![WhatsApp Group](https://img.shields.io/badge/WhatsApp-Group-25D366?logo=whatsapp)](https://chat.whatsapp.com/KsxrUGIPWvUBYAjI1ogaGs)
[![Telegram Group](https://img.shields.io/badge/Telegram-Group-32AFED?logo=telegram)](https://t.me/apigratisoficial)

## Obtenha suas credenciais
https://apigratis.com.br

# Mais informações

https://pypi.org/project/apigratis/0.0.9/

## Serviços de API disponíveis

| Up  | Services available            | Description       | Free    | Beta        | Stable   |
------|-------------------------------|-------------------|---------| ------------------------- | ------------------------- |
| ✅ | WhatsAppService                | API do WhatsApp Gratuita.               |   ✅   | ✅                   | ⌛                   |
| ✅ | Receita Data CNPJ              | API Dados CNPJ Receita.                 |   ⌛   | ⌛                   | ⌛                   |
| ✅ | Receita Data CPF               | API Dados de CPF Serasa.                |   ⌛   | ⌛                   | ⌛                   |
| ✅ | CorreiosService                | API Busca encomendas Correios Brazil.   |   ⌛   | ⌛                   | ⌛                   |
| ✅ | CEPLocation                    | API CEP Geolocation + IBGE Brazil.      |   ⌛   | ⌛                   | ⌛                   |
| ✅ | VehiclesService                | API Placa Dados.                        |   ⌛   | ⌛                   | ⌛                   |
| ✅ | FipeService                    | API Placa FIPE.                         |   ⌛   | ⌛                   | ⌛                   |

# Como utilizar

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