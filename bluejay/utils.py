from typing import Any, List, Optional

import dbus
import dbus.service

from .constants import (
    ADAPTER_INTERFACE,
    BLUEZ_SERVICE_NAME,
    DBUS_OM_IFACE,
    DBUS_PROPERTIES,
    DEVICE_INTERFACE,
    GATT_MANAGER_INTERFACE,
)


def is_empty_array(arr: Optional[list]):
    if arr:
        return len(arr) == 0
    return True


def is_empty_dict(dic: Optional[dict]):
    if dic:
        return len(dic.keys()) == 0
    return True


def find_adapter(bus: dbus.SystemBus):
    object_manager = dbus.Interface(
        bus.get_object(BLUEZ_SERVICE_NAME, "/"),
        DBUS_OM_IFACE,
    )
    objects = object_manager.GetManagedObjects()

    for (
        obj,
        props,
    ) in objects.items():
        if GATT_MANAGER_INTERFACE in props.keys():
            adapter_props = dbus.Interface(
                bus.get_object(BLUEZ_SERVICE_NAME, obj),
                DBUS_PROPERTIES,
            )
            try:
                adapter_props.Set(ADAPTER_INTERFACE, "Powered", dbus.Boolean(True))
                adapter_props.Set(ADAPTER_INTERFACE, "Pairable", dbus.Boolean(False))
            except dbus.DBusException:
                print("Cannot set dbus properties")

            return obj

    return None


def disconnect_connected_devices(bus: dbus.SystemBus):
    object_manager = dbus.Interface(
        bus.get_object(BLUEZ_SERVICE_NAME, "/"),
        DBUS_OM_IFACE,
    )
    objects = object_manager.GetManagedObjects()
    path = None
    for object_path, props in objects.items():
        device = props.get(DEVICE_INTERFACE, None)
        if device is None:
            continue

        dev_iface = dbus.Interface(
            bus.get_object(BLUEZ_SERVICE_NAME, object_path),
            DEVICE_INTERFACE,
        )
        dev_iface.Disconnect()


def get_hostname(bus: dbus.SystemBus) -> str:
    interface = dbus.Interface(
        bus.get_object(
            "org.freedesktop.hostname1",
            "/org/freedesktop/hostname1",
        ),
        "org.freedesktop.DBus.Properties",
    )

    return str(interface.Get("org.freedesktop.hostname1", "Hostname"))


def isinstances(data, *instances):
    for instance in instances:
        if isinstance(data, instance):
            return True

    return False


def dbus_to_python(data) -> Any:
    if isinstances(data, dbus.String, dbus.ObjectPath):
        return str(data)
    if isinstance(data, dbus.Boolean):
        return bool(data)
    if isinstances(
        data,
        dbus.Int16,
        dbus.Int32,
        dbus.Int64,
        dbus.UInt16,
        dbus.UInt32,
        dbus.UInt64,
        dbus.Byte,
    ):
        return int(data)
    if isinstance(data, dbus.Double):
        return float(data)
    if isinstances(data, dbus.Array, list):
        return [dbus_to_python(element) for element in data]
    if isinstance(data, dbus.Dictionary):
        return {str(key): dbus_to_python(value) for key, value in data.items()}


def dbus_to_string(data) -> str:
    return "".join([chr(byte) for byte in dbus_to_python(data)])


def bytes_to_dbus_bytes(bytes: List[int]):
    return [dbus.Byte(byte) for byte in bytes]


def string_to_bytes(data: str):
    return [dbus.Byte(ord(chr)) for chr in data]
