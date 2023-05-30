# more endpoints
# https://apibrasil.com.br/documentacoes
#!/usr/bin/env python

from apigratis.Service import Service
import json

def main():

    json_data = {
        "action": "sendText",
        "credentials": {
            "SecretKey": "secretKey",
            "PublicToken": "publicToken",
            "DeviceToken": "deviceToken",
            "BearerToken": "bearerToken"
        },
        "body": {
            "message": "Hello World",
            "phone": "5511999999999",
            "time_typing": 1
        }
    }

    teste = Service.whatsapp(json.dumps(json_data))

    print(teste)

if __name__ == "__main__":
    main()
