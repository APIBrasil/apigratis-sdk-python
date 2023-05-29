import requests
import json

class ServiceClass:

    def __init__(self, data):
        self.credentials = data.credentials
        self.server = "https://cluster-01.apigratis.com/api/v1/"

    def whatsapp(self, data):

        url = "whatsapp/"+data.body.action
        payload = json.dumps(data.body)
        
        headers = {
            'Content-Type': 'application/json',
            'SecretKey': self.credentials.SecretKey,
            'PublicToken': self.PublicToken,
            'Authorization': 'Bearer ' + self.credentials.BearerToken,
            'DeviceToken': self.DeviceToken
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return json.loads(response.text.encode('utf8'))

