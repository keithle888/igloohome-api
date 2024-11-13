import json

import aiohttp
from dacite import from_dict

from src.igloohome_api_keithle888.auth import Auth
from src.igloohome_api_keithle888.models.get_devices_response import GetDevicesResponse

_BASE_URL = "https://api.igloodeveloper.co"
_BASE_PATH = "igloohome"
_DEVICES_PATH_SEGMENT = "devices"


class Api:
    def __init__(
            self,
            auth: Auth,
            host: str = _BASE_URL
    ):
        self.auth = auth
        self.host = host

    async def get_devices(self) -> GetDevicesResponse:
        response = await self.auth.request(
            "get",
            f'{self.host}/{_BASE_PATH}/{_DEVICES_PATH_SEGMENT}',
        )
        if response.status == 200:
            return from_dict(GetDevicesResponse, await response.json())
        else:
            raise ApiException("Response failure", response.status)


class ApiException(Exception):
    def __init__(self, message: str, response_code: int):
        self.message = message
        self.response_code = response_code

    def __str__(self):
        return f'ApiException(message={self.message}, response_code={self.response_code})'


async def _create_exception(response: aiohttp.ClientResponse) -> ApiException:
    return ApiException(
        message=f'Unsuccessful request. code={response.status}, message={await response.text()}',
        response_code=response.status
    )
