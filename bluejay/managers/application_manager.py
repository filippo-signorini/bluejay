from typing import Optional

import dbus
import dbus.service

from ..constants import BLUEZ_SERVICE_NAME, GATT_MANAGER_INTERFACE
from ..interfaces.gatt import Application
from ..types import DBUSErrorCallback, NoneCallback


class ApplicationManager:
    def __init__(self, bus: dbus.SystemBus, adapter: dbus.service.Object):
        self._interface = dbus.Interface(
            bus.get_object(BLUEZ_SERVICE_NAME, adapter),
            GATT_MANAGER_INTERFACE,
        )

    def register_application(
        self,
        app: Application,
        on_success: Optional[NoneCallback] = None,
        on_error: Optional[DBUSErrorCallback] = None,
    ):
        self._interface.RegisterApplication(
            app.get_path(),
            {},
            reply_handler=on_success,
            error_handler=on_error,
        )

    def unregister_application(
        self,
        app: Application,
        on_success: Optional[NoneCallback] = None,
        on_error: Optional[DBUSErrorCallback] = None,
    ):
        self._interface.UnregisterApplication(
            app.get_path(),
            reply_handler=on_success,
            error_handler=on_error,
        )
