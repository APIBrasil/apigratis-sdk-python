from apigratis.Service import Service
import json

def main():

    Service.whatsapp('null', {
        'action': 'sendText',
        'credentials': {
            'SecretKey': 'secretKey',
            'PublicToken': 'publicToken',
            'DeviceToken': 'deviceToken',
            'BearerToken': 'bearerToken'
        },
        'body': {
            'message': 'Hello World',
            'phone': '5511999999999',
            'time_typing': 1
        }
    })

if __name__ == '__main__':
    main()
