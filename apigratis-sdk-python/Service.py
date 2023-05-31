import requests
import json

class Service:

    def whatsapp(dados):

        try:
            server = "https://cluster-01.apigratis.com/api/v1/whatsapp/"

            data = json.loads(dados)

            if not data['action']:
                raise Exception('Action não informada, verifique a documentação')

            action = data['action']

            url = server+str(action)

            if not data['body']:
                raise Exception('Body não informado, verifique a documentação')

            payload = json.dumps(data['body'])

            credentials = data['credentials']

            if not credentials['SecretKey']:
                raise Exception('SecretKey não informado')
            if not credentials['PublicToken']:
                raise Exception('PublicToken não informado')
            if not credentials['BearerToken']:
                raise Exception('BearerToken não informado')
            if not credentials['DeviceToken']:
                raise Exception('DeviceToken não informado')

            headers = {
                'Content-Type': 'application/json',
                'SecretKey': credentials['SecretKey'],
                'PublicToken': credentials['PublicToken'],
                'Authorization': 'Bearer ' + credentials['BearerToken'],
                'DeviceToken': credentials['DeviceToken']
            }

            agent = 'APIBRASIL\Whatsapp/1.0.0' 

            headers['User-Agent'] = agent

            response = requests.request("POST", url, headers=headers, data=payload, allow_redirects=False, stream=True, proxies=None)

            return json.loads(response.text.encode('utf8'))

        except Exception as e:
            return {'error': str(e)}