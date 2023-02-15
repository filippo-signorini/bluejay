import dbus
import dbus.service

from ..constants import (
    AGENT_INTERFACE,
    BLUEZ_SERVICE_NAME,
    DBUS_PROPERTIES,
    DEVICE_INTERFACE,
)
from ..enums import AgentCapability
from ..exceptions import RejectedException


class Agent(dbus.service.Object):
    def __init__(
        self,
        bus: dbus.SystemBus,
        path: str,
        capability: AgentCapability,
    ):
        self.bus = bus
        self.path = f"{path}/agent"
        self.capability = capability
        super().__init__(bus, path)

    def get_path(self):
        return dbus.ObjectPath(self.path)

    @dbus.service.method(AGENT_INTERFACE, in_signature="", out_signature="")
    def Release(self):
        pass

    @dbus.service.method(AGENT_INTERFACE, in_signature="os", out_signature="")
    def AuthorizeService(self, device, uuid: str):
        print(f"AuthorizeService ({device}, {uuid})")
        authorize = input("Authorize connection (y/n): ")
        if authorize == "y":
            return
        raise RejectedException("Connection rejected by user")

    @dbus.service.method(AGENT_INTERFACE, in_signature="o", out_signature="s")
    def RequestPinCode(self, device):
        print(f"RequestPinCode ({device})")
        self._set_trusted(device)
        return input("Enter PIN Code: ")

    @dbus.service.method(AGENT_INTERFACE, in_signature="o", out_signature="u")
    def RequestPasskey(self, device):
        print(f"RequestPasskey ({device})")
        self._set_trusted(device)
        passkey = input("Enter passkey: ")
        return dbus.UInt32(passkey)

    @dbus.service.method(AGENT_INTERFACE, in_signature="ouq", out_signature="")
    def DisplayPasskey(self, device, passkey, entered):
        print(f"DisplayPaskey ({device}, {passkey}, {entered})")

    @dbus.service.method(AGENT_INTERFACE, in_signature="os", out_signature="")
    def DisplayPinCode(slef, device, pincode):
        print(f"DisplayPinCode ({device}, {pincode})")

    @dbus.service.method(AGENT_INTERFACE, in_signature="ou", out_signature="")
    def RequestConfirmation(self, device, passkey):
        print(f"RequestConfirmation ({device}, {passkey})")
        confirm = input("Confirm passkey (y/n): ")
        if confirm == "y":
            self._set_trusted(device)
            return
        raise RejectedException("Passkey doesn't match")

    @dbus.service.method(AGENT_INTERFACE, in_signature="o", out_signature="")
    def RequestAuthorization(self, device):
        print(f"RequestAuthorization ({device})")
        auth = input("Authorize (y/n): ")
        if auth == "y":
            return
        raise RejectedException("Pairing Rejected")

    @dbus.service.method(AGENT_INTERFACE, in_signature="", out_signature="")
    def Cancel(self):
        print("Cancel")

    def _set_trusted(self, path):
        print(f"Set Trusted {path}")
        # props = dbus.Interface(
        #     self.bus.get_object(BLUEZ_SERVICE_NAME, path),
        #     DBUS_PROPERTIES,
        # )
        # props.Set(DEVICE_INTERFACE, "Trusted", True)
