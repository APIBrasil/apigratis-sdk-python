from api_brasil.api_client.client_builder import APIBrasilClient

from abc import ABC


class APIBrasilFeature(ABC):
    """The interface for implement APIBrasil Features"""

    def __init__(self, api_brasil_client: APIBrasilClient, device_token: str):
        pass
