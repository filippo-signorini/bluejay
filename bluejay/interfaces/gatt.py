import typing

import dbus
import dbus.service

from ..constants import (
    ADVERTISEMENT_INTERFACE,
    DBUS_OM_IFACE,
    DBUS_PROPERTIES,
    GATT_CHARACTERISTIC_INTERFACE,
    GATT_DESCRIPTOR_INTERFACE,
    GATT_SERVICE_INTERFACE,
)
from ..enums import CharacteristicFlag, DescriptorFlag
from ..exceptions import InvalidArgsException, NotSupportedException


class Application(dbus.service.Object):
    def __init__(self, bus: dbus.SystemBus, path: str):
        self.path = path
        self.bus = bus
        self.services: typing.List[Service] = []
        super().__init__(bus, path)

    def get_path(self):
        return dbus.ObjectPath(self.path)

    def add_service(self, service: "Service"):
        self.services.append(service)

    @dbus.service.method(DBUS_OM_IFACE, out_signature="a{oa{sa{sv}}}")
    def GetManagedObjects(self):  # pylint: disable=invalid-name
        response = {}
        for serv in self.services:
            response[serv.get_path()] = serv.get_properties()
            for char in serv.get_characteristics():
                response[char.get_path()] = char.get_properties()
                for desc in char.get_descriptors():
                    response[desc.get_path()] = desc.get_properties()

        return response


class Service(dbus.service.Object):
    """Base Service class"""

    def __init__(
        self,
        bus: dbus.SystemBus,
        path_base: str,
        index: int,
        uuid: str,
        primary: bool,
    ):  # pylint: disable=too-many-arguments
        self.path = f"{path_base}/service{index}"
        self.bus = bus
        self.uuid = uuid
        self.primary = primary
        self.characteristics: typing.List[Characteristic] = []
        super().__init__(bus, self.path)

    def get_properties(self):
        return {
            GATT_SERVICE_INTERFACE: {
                "UUID": self.uuid,
                "Primary": self.primary,
                "Characteristics": dbus.Array(
                    self.get_characteristic_paths(), signature="o"
                ),
            }
        }

    def get_path(self):
        return dbus.ObjectPath(self.path)

    def add_characteristic(self, characteristic: "Characteristic"):
        self.characteristics.append(characteristic)

    def get_characteristic_paths(self):
        return [char.get_path() for char in self.characteristics]

    def get_characteristics(self):
        return self.characteristics

    @dbus.service.method(DBUS_PROPERTIES, in_signature="s", out_signature="a{sv}")
    def GetAll(self, interface):  # pylint: disable=invalid-name
        if interface != GATT_SERVICE_INTERFACE:
            raise InvalidArgsException()
        return self.get_properties()[GATT_SERVICE_INTERFACE]

    @dbus.service.method(ADVERTISEMENT_INTERFACE, in_signature="", out_signature="")
    def Release(self):  # pylint: disable=invalid-name
        print(f"{self.path}: Released")


class Characteristic(dbus.service.Object):
    """Base Characteritic class"""

    def __init__(
        self,
        bus: dbus.SystemBus,
        index: int,
        uuid: str,
        flags: typing.List[CharacteristicFlag],
        service: Service,
    ):  # pylint: disable=too-many-arguments
        self.path = f"{service.path}/char{index}"
        self.bus = bus
        self.uuid = uuid
        self.service = service
        self.flags = flags
        self.descriptors: typing.List[Descriptor] = []
        super().__init__(bus, self.path)

    def get_properties(self):
        return {
            GATT_CHARACTERISTIC_INTERFACE: {
                "Service": self.service.get_path(),
                "UUID": self.uuid,
                "Flags": [flag.value for flag in self.flags],
                "Descriptors": dbus.Array(self.get_descriptor_paths(), signature="o"),
            }
        }

    def get_path(self):
        return dbus.ObjectPath(self.path)

    def add_descriptor(self, descriptor: "Descriptor"):
        self.descriptors.append(descriptor)

    def get_descriptor_paths(self):
        return [desc.get_path() for desc in self.descriptors]

    def get_descriptors(self):
        return self.descriptors

    @dbus.service.method(DBUS_PROPERTIES, in_signature="s", out_signature="a{sv}")
    def GetAll(
        self,
        interface,
    ):  # pylint: disable=invalid-name
        if interface != GATT_CHARACTERISTIC_INTERFACE:
            raise InvalidArgsException()

        return self.get_properties()[GATT_CHARACTERISTIC_INTERFACE]

    @dbus.service.method(
        GATT_CHARACTERISTIC_INTERFACE, in_signature="a{sv}", out_signature="ay"
    )
    def ReadValue(
        self,
        options,  # pylint: disable=unused-argument
    ):  # pylint: disable=invalid-name
        print(f"{self.path}: Default ReadValue called, returning error")
        raise NotSupportedException()

    @dbus.service.method(GATT_CHARACTERISTIC_INTERFACE, in_signature="aya{sv}")
    def WriteValue(
        self,
        value: typing.List[int],  # pylint: disable=unused-argument
        options: typing.Dict[str, typing.Any],  # pylint: disable=unused-argument
    ):  # pylint: disable=invalid-name
        print(f"{self.path}: Default WriteValue called, returning error")
        raise NotSupportedException()

    @dbus.service.method(GATT_CHARACTERISTIC_INTERFACE)
    def StartNotify(self):  # pylint: disable=invalid-name
        print("Default StartNotify called, returning error")
        raise NotSupportedException()

    @dbus.service.method(GATT_CHARACTERISTIC_INTERFACE)
    def StopNotify(self):  # pylint: disable=invalid-name
        print("Default StopNotify called, returning error")
        raise NotSupportedException()

    def emitPropertiesChanged(
        self,
        changed,
        interface=GATT_CHARACTERISTIC_INTERFACE,
        invalidated=[],
    ):
        self.PropertiesChanged(interface, changed, invalidated)

    @dbus.service.signal(DBUS_PROPERTIES, signature="sa{sv}as")
    def PropertiesChanged(
        self,
        interface,
        changed,
        invalidated,
    ):  # pylint: disable=invalid-name
        pass


class Descriptor(dbus.service.Object):
    """Base Descriptor class"""

    def __init__(
        self,
        bus: dbus.SystemBus,
        index: int,
        uuid: str,
        flags: typing.List[DescriptorFlag],
        characteristic: Characteristic,
    ):  # pylint: disable=too-many-arguments
        self.path = f"{characteristic.path}/desc{index}"
        self.bus = bus
        self.uuid = uuid
        self.flags = flags
        self.characteristic = characteristic
        super().__init__(bus, self.path)

    def get_properties(self):
        return {
            GATT_DESCRIPTOR_INTERFACE: {
                "Characteristic": self.characteristic.get_path(),
                "UUID": self.uuid,
                "Flags": self.flags,
            }
        }

    def get_path(self):
        return dbus.ObjectPath(self.path)

    @dbus.service.method(DBUS_PROPERTIES, in_signature="s", out_signature="a{sv}")
    def GetAll(self, interface):  # pylint: disable=invalid-name
        if interface != GATT_DESCRIPTOR_INTERFACE:
            raise InvalidArgsException()
        return self.get_properties()[GATT_DESCRIPTOR_INTERFACE]

    @dbus.service.method(
        GATT_DESCRIPTOR_INTERFACE, in_signature="a{sv}", out_signature="ay"
    )
    def ReadValue(
        self,
        options,  # pylint: disable=unused-argument
    ):  # pylint: disable=invalid-name
        print(f"{self.path}: Default ReadValue called, returning error")
        raise NotSupportedException()

    @dbus.service.method(GATT_DESCRIPTOR_INTERFACE, in_signature="aya{sv}")
    def WriteValue(
        self,
        value,  # pylint: disable=unused-argument
        options,  # pylint: disable=unused-argument
    ):  # pylint: disable=invalid-name
        print(f"{self.path}: Default WriteValue called, returning error")
        raise NotSupportedException()
