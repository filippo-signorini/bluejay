from typing import Any, Callable, Optional

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

from dbus.exceptions import DBusException

from .interfaces.gatt import Application

NoneCallback = Callable[[], None]
DBUSErrorCallback = Callable[[DBusException], None]
DeviceEventCallback = Callable[[Any], None]
AdvertsementChangeCallback = Callable[[bool, Optional[DBusException]], None]
ApplicationChangedCallback = Callable[
    [
        Literal["registered", "unregistered", "error"],
        Optional[DBusException],
    ],
    None,
]
