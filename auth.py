import aiohttp
import jwt

OAUTH2_TOKEN_URL = "https://auth.igloohome.co/oauth2/token"
OAUTH2_SCOPE = "igloohomeapi/algopin-hourly"


class Auth:
    def __init__(self, session: aiohttp.ClientSession, host: str, client_id: str, client_secret: str):
        self.access_token = None
        self.session = session
        self.client_id = client_id
        self.client_secret = client_secret
        self.host = host

    async def async_get_access_token(self) -> str:
        form = aiohttp.FormData()
        form.add_field("grant_type", "client_credentials")
        form.add_field("scope", OAUTH2_SCOPE)
        response = await self.session.post(
            url=OAUTH2_TOKEN_URL,
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

    async def request(self, method: str, path: str, **kwargs) -> aiohttp.ClientResponse:
        """Make a request."""
        headers = kwargs.get("headers")

        if headers is None:
            headers = {}
        else:
            headers = dict(headers)

        headers["authorization"] = await self.async_get_valid_access_token()

        return await self.session.request(
            method, f"{self.host}/{path}", **kwargs, headers=headers,
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
