from enum import Enum
from api_brasil.api_client.client_builder import APIBrasilClient
from api_brasil.features.interfaces import APIBrasilFeature


class Endpoints(Enum):
    """Enum class to represent the endpoints of the Vehicles API."""

    fipe = "fipe"
    dados = "dados"


class VehiclesApi(APIBrasilFeature):
    """Class to interact with the Vehicles API."""

    def __init__(self, api_brasil_client: APIBrasilClient, device_token: str):
        self.api_brasil_client = api_brasil_client
        self.device_token = device_token

    def set_plate(self, plate: str):
        """Set the plate to be used in the API requests"""
        self.plate = plate

    def consulta(self, vechiles_api_endpoint: Endpoints = Endpoints.dados) -> tuple:
        """Method to consult the API with the plate set in the class."""
        endpoint = f"/vehicles/{vechiles_api_endpoint.value}"

        if not self.plate:
            raise ValueError(
                "The plate is not set. Use the 'set_plate' method to set the plate."
            )

        response, status_code = self.api_brasil_client.post_request(
            endpoint=endpoint,
            device_token=self.device_token,
            body={
                "placa": self.plate,
            },
        )

        return response, status_code
