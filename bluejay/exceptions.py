import dbus
import dbus.exceptions


class InvalidArgsException(dbus.exceptions.DBusException, Exception):
    _dbus_error_name = "org.freedesktop.DBus.Error.InvalidArgs"


class NotSupportedException(dbus.exceptions.DBusException, Exception):
    _dbus_error_name = "org.bluez.Error.NotSupported"


class NotPermittedException(dbus.exceptions.DBusException, Exception):
    _dbus_error_name = "org.bluez.Error.NotPermitted"


class NotAuthorizedException(dbus.exceptions.DBusException, Exception):
    _dbus_error_name = "org.bluez.Error.NotAuthorized"


class InvalidValueLengthException(dbus.exceptions.DBusException, Exception):
    _dbus_error_name = "org.bluez.Error.InvalidValueLength"


class RejectedException(dbus.exceptions.DBusException, Exception):
    _dbus_error_name = "org.bluez.Error.Rejected"


class FailedException(dbus.exceptions.DBusException, Exception):
    _dbus_error_name = "org.bluez.Error.Failed"
