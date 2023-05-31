# more endpoints
# https://apibrasil.com.br/documentacoes
#!/usr/bin/env python

from apigratis.Service import Service
import json

def sendText():

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

    sendText = Service.whatsapp(json.dumps(json_data))

    print(sendText)

if __name__ == "__main__":
    sendText()
