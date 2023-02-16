from typing import Optional

import dbus
import dbus.service

from ..constants import ADVERTISING_MANAGER_INTERFACE, BLUEZ_SERVICE_NAME
from ..interfaces.advertisement import Advertisement
from ..types import DBUSErrorCallback, NoneCallback


class AdvertisingManager:
    def __init__(self, bus: dbus.SystemBus, adapter: dbus.service.Object):
        self._interface = dbus.Interface(
            bus.get_object(BLUEZ_SERVICE_NAME, adapter),
            ADVERTISING_MANAGER_INTERFACE,
        )

    def register_advertisement(
        self,
        ad: Advertisement,
        on_success: Optional[NoneCallback] = None,
        on_error: Optional[DBUSErrorCallback] = None,
    ):
        self._interface.RegisterAdvertisement(
            ad.get_path(),
            {},
            reply_handler=on_success,
            error_handler=on_error,
        )

    def unregister_advertisement(
        self,
        ad: Advertisement,
        on_success: Optional[NoneCallback] = None,
        on_error: Optional[DBUSErrorCallback] = None,
    ):
        self._interface.UnregisterAdvertisement(
            ad.get_path(),
            reply_handler=on_success,
            error_handler=on_error,
        )
