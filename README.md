# igloohome-api
A python HTTP library based on `aiohttp` to make use of [igloohome's REST API](https://igloocompany.stoplight.io/docs/igloohome-api/1w1cuv56ge5xq-overview).
This library is designed to be used via the [iglooaccess](https://www.igloocompany.co/iglooaccess) service.

## Requirements
An account on the iglooaccess portal needs to be created to get a `client_id` & `client_secret` for authentication.

## Usage

### Authentication
```python
from igloohome_api import Auth
from aiohttp import ClientSession

session = ClientSession()
auth = Auth(
    client_id="<client_id>",
    client_secret="<client_secret>",
    session=session,
)
```

### API usage
```python
from igloohome_api import Api

api = Api(auth)

devices = await api.get_devices()
```
