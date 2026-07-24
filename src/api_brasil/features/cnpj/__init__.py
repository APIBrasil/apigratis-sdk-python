from api_brasil.api_client.client_builder import APIBrasilClient
from api_brasil.features.interfaces import APIBrasilFeature


class CNPJApi(APIBrasilFeature):
    """Class to interact with the Vehicles API."""

    def __init__(self, api_brasil_client: APIBrasilClient, device_token: str):
        self.api_brasil_client = api_brasil_client
        self.device_token = device_token

    def set_cnpj(self, cnpj: str):
        """Set the plate to be used in the API requests"""
        self.cnpj = cnpj

    def consulta(self) -> tuple:
        """Method to consult the API with the plate set in the class."""
        endpoint = "/dados/cnpj"

        if not self.cnpj:
            raise ValueError(
                "The CNPJ number is not set. Use the 'set_cnpj' method to set the CNPJ."
            )

        response, status_code = self.api_brasil_client.post_request(
            endpoint=endpoint,
            device_token=self.device_token,
            body={
                "cnpj": self.cnpj,
            },
        )

        return response, status_code
