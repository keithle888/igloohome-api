import aiohttp
import jwt

_OAUTH2_HOST = "https://auth.igloohome.co"
_OAUTH2_TOKEN_PATH = "/oauth2/token"
_OAUTH2_SCOPE_EVERYTHING = OAUTH2_SCOPE = "igloohomeapi/algopin-hourly igloohomeapi/algopin-daily igloohomeapi/algopin-permanent igloohomeapi/algopin-onetime igloohomeapi/create-pin-bridge-proxied-job igloohomeapi/delete-pin-bridge-proxied-job igloohomeapi/lock-bridge-proxied-job igloohomeapi/unlock-bridge-proxied-job igloohomeapi/get-devices igloohomeapi/get-job-status igloohomeapi/get-properties"


class Auth:
    def __init__(
            self,
            session: aiohttp.ClientSession,
            client_id: str,
            client_secret: str,
            host: str = _OAUTH2_HOST,
            scope: str = _OAUTH2_SCOPE_EVERYTHING,
    ) -> None:
        self.access_token = None
        self.session = session
        self.client_id = client_id
        self.client_secret = client_secret
        self.host = host
        self.scope = scope

    async def async_get_access_token(self) -> str:
        form = aiohttp.FormData()
        form.add_field("grant_type", "client_credentials")
        form.add_field("scope", self.scope)
        response = await self.session.post(
            url=self.host + _OAUTH2_TOKEN_PATH,
            auth=aiohttp.BasicAuth(
                login=self.client_id, password=self.client_secret
            ),
            data=form,
        )
        json = await response.json()
        if response.status == 200:
            self.access_token = json["access_token"]
            return self.access_token
        else:
            raise AuthException(f'Failed to get access token. responseCode=${response.status}')

    async def async_get_valid_access_token(self) -> str:
        """Gets a valid access token."""
        if self.access_token is None:
            access_token = await self.async_get_access_token()
            return access_token
        elif is_access_token_valid(self.access_token):
            return self.access_token
        else:
            return await self.async_get_access_token()

    async def request(self, method: str, url: str, **kwargs) -> aiohttp.ClientResponse:
        """Make a request."""
        headers = kwargs.get("headers")

        if headers is None:
            headers = {}
        else:
            headers = dict(headers)

        headers["Authorization"] = f"Bearer {await self.async_get_valid_access_token()}"
        headers["Accept"] = "application/json"

        return await self.session.request(
            method, url, **kwargs, headers=headers,
        )


def is_access_token_valid(access_token: str) -> bool:
    """Check if the access token is valid."""
    try:
        # Expiry is automatically verified during decoding. Will raise ExpiredSignatureError.
        # See: https://pyjwt.readthedocs.io/en/stable/usage.html#expiration-time-claim-exp
        claims = jwt.decode(access_token, options={"require": ["exp"]})
    except Exception:
        return False


class AuthException(Exception):
    pass