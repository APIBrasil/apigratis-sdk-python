from api_brasil.api_client.client_builder import APIBrasilClient
from api_brasil.features.interfaces import APIBrasilFeature


class CEPGeoLocationAPI(APIBrasilFeature):
    """Class to interact with the Vehicles API."""

    def __init__(self, api_brasil_client: APIBrasilClient, device_token: str):
        self.api_brasil_client = api_brasil_client
        self.device_token = device_token

    def set_cep(self, cep: str):
        """Set the plate to be used in the API requests"""
        self.cep = cep

    def consulta(self) -> tuple:
        """Method to consult the API with the plate set in the class."""
        endpoint = "/cep/cep"

        if not self.cep:
            raise ValueError(
                "The CEP number is not set. Use the 'set_cep' method to set the CEP."
            )

        response, status_code = self.api_brasil_client.post_request(
            endpoint=endpoint,
            device_token=self.device_token,
            body={
                "cep": self.cep,
            },
        )

        return response, status_code
