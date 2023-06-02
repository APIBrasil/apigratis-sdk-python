import requests
import json

class Service:

    server = None

    def __init__(self):
        self.server = "https://cluster-01.apigratis.com/api/v1/"

    def request(self, service, dados):
        try:
            
            action = data.get('action', '')
            data = json.loads(dados)

            credentials = data['credentials']
            payload = json.dumps(data['body'])

            url = self.server + str(service) + str(action)

            headers = {
                'Content-Type': 'application/json',
                'SecretKey': credentials['SecretKey'],
                'PublicToken': credentials['PublicToken'],
                'Authorization': 'Bearer ' + credentials['BearerToken'],
                'DeviceToken': credentials['DeviceToken']
            }

            agent = 'APIBRASIL/PYTHON-SDK'
            headers['User-Agent'] = agent

            response = requests.request("POST", url, headers=headers, data=payload, allow_redirects=False, stream=True, proxies=None)

            return json.loads(response.text.encode('utf8')) 

        except Exception as e:
            return {'error': str(e)}

    def whatsapp(self, dados):
        return self.request('whatsapp', dados)

    def vehicles(self, dados):
        return self.request('vehicles', dados)

    def correios(self, dados):
        return self.request('correios', dados)

    def cep(self, dados):
        return self.request('cep', dados)

    def cnpj(self, dados):
        return self.request('dados/cnpj', dados)

    def cpf(self, dados):
        return self.request('dados/cpf', dados)
