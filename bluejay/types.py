from typing import Any, Callable, Literal, Optional

from dbus.exceptions import DBusException

from .interfaces.gatt import Application

NoneCallback = Callable[[], None]
DBUSErrorCallback = Callable[[DBusException], None]
DeviceEventCallback = Callable[[Any], None]
AdvertsementChangeCallback = Callable[[bool, Optional[DBusException]], None]
ApplicationChangedCallback = Callable[
    [
        Application,
        Literal["registered", "unregistered", "error"],
        Optional[DBusException],
    ],
    None,
]
