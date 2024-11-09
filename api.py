from auth import Auth


class Api:
    def __init__(self, auth: Auth):
        self.auth = auth

    async def get_devices(self) -> [dict]:
        response = await self.auth.request(
            "get",
            "igloohome/devices",
        )
        if response.status == 200:
            return await response.json()
        else:
            raise ApiException("Response failed", response.status)


class ApiException(Exception):
    def __init__(self, message: str, response_code: int):
        self.message = message
        self.response_code = response_code



