import requests
import json

class Service:

    def whatsapp(self, data):

        server = "https://cluster-01.apigratis.com/api/v1/whatsapp/"

        url = server+data.action
        payload = json.dumps(data.body)

        credentials = data.credentials

        headers = {
            'Content-Type': 'application/json',
            'SecretKey': credentials.SecretKey,
            'PublicToken': credentials.PublicToken,
            'Authorization': 'Bearer ' + credentials.BearerToken,
            'DeviceToken': credentials.DeviceToken
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return json.loads(response.text.encode('utf8'))