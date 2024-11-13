from dataclasses import dataclass
from typing import Any


@dataclass
class GetDevicesResponsePayload:
    id: str
    type: str
    deviceId: str
    deviceName: str
    pairedAt: str
    homeId: Any
    linkedDevices: Any


@dataclass
class GetDevicesResponse:
    nextCursor: str
    payload: list[GetDevicesResponsePayload]
