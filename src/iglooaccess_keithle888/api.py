import aiohttp

from auth import Auth

BASE_PATH = "igloohome"
DEVICES_PATH_SEGMENT = "devices"
DEVICES_PATH = BASE_PATH + "/" + DEVICES_PATH_SEGMENT
ALGOPIN_PATH_SEGMENT = "algopin"


class Api:
    def __init__(self, auth: Auth):
        self.auth = auth

    async def get_devices(self):
        response = await self.auth.request(
            "get",
            DEVICES_PATH,
        )
        if response.status == 200:
            return await response.json()
        else:
            raise ApiException("Response failure", response.status)

    async def get_device_info(self, device_id: str):
        response = await self.auth.request(
            "get",
            f'{DEVICES_PATH}/{device_id}',
        )
        if response.status == 200:
            return await response.json()
        else:
            raise await _create_exception(response)

    # async def generate_algopin_onetime(
    #         self,
    #         device_id: str,
    #         variance: int,
    #         start_date: str,
    #         access_name: str
    # ):
    #     response = await self.auth.request(
    #         method="get",
    #         path=f'{DEVICES_PATH}/{device_id}/{ALGOPIN_PATH_SEGMENT}/onetime',
    #         json={
    #             "variance": variance,
    #             "startDate": start_date,
    #             "accessName": access_name
    #         }
    #     )
    #     if response.status == 200:
    #         return await response.json()
    #     else:
    #         raise await _create_exception(response)


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
