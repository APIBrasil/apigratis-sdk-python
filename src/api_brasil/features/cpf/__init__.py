from api_brasil.api_client.client_builder import APIBrasilClient
from api_brasil.features.interfaces import APIBrasilFeature


class CPFApi(APIBrasilFeature):
    """Class to interact with the Vehicles API."""

    def __init__(self, api_brasil_client: APIBrasilClient, device_token: str):
        self.api_brasil_client = api_brasil_client
        self.device_token = device_token

    def set_cpf(self, cpf: str):
        """Set the plate to be used in the API requests"""
        self.cpf = cpf

    def consulta(self) -> tuple:
        """Method to consult the API with the plate set in the class."""
        endpoint = "/dados/cpf"

        if not self.cpf:
            raise ValueError(
                "The cpf number is not set. Use the 'set_cpf' method to set the cpf."
            )

        response, status_code = self.api_brasil_client.post_request(
            endpoint=endpoint,
            device_token=self.device_token,
            body={
                "cpf": self.cpf,
            },
        )

        return response, status_code
