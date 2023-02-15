import typing

import dbus

NoneCallback = typing.Callable
DBUSErrorCallback = typing.Callable[[dbus.exceptions.DBusException], None]
DeviceEventCallback = typing.Callable[[typing.Any], None]
