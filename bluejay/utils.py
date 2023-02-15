from typing import Optional, Union

import dbus
import dbus.service

from .constants import (
    ADAPTER_INTERFACE,
    BLUEZ_SERVICE_NAME,
    DBUS_OM_IFACE,
    DBUS_PROPERTIES,
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
            adapter_props.Set(ADAPTER_INTERFACE, "Powered", dbus.Boolean(True))
            adapter_props.Set(ADAPTER_INTERFACE, "Pairable", dbus.Boolean(False))
            return obj

    return None


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


def dbus_to_python(data):
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
    if isinstance(data, dbus.Array):
        return [dbus_to_python(element) for element in data]
    if isinstance(data, dbus.Dictionary):
        return {key: dbus_to_python(value) for key, value in data.items()}
