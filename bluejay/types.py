import typing

import dbus

NoneCallback = typing.Callable[[], None]
DBUSErrorCallback = typing.Callable[[dbus.exceptions.DBusException], None]
DeviceEventCallback = typing.Callable[[typing.Any], None]
AdvertsementChangeCallback = typing.Callable[
    [bool, typing.Optional[dbus.exceptions.DBusException]], None
]
