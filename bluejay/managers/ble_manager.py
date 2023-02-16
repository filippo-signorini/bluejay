import threading
from typing import Optional

import dbus
import dbus.service

from ..constants import DBUS_OM_IFACE, DBUS_PROPERTIES, DEVICE_INTERFACE
from ..glib import GLib
from ..interfaces.advertisement import Advertisement
from ..interfaces.agent import Agent
from ..interfaces.gatt import Application
from ..types import AdvertsementChangeCallback, DeviceEventCallback
from ..utils import find_adapter
from .advertising_manager import AdvertisingManager
from .agent_manager import AgentManager
from .application_manager import ApplicationManager


class BLEManager:
    def __init__(self, base_path: str, run_mainloop=True, debug=False):
        self.base_path = base_path
        self.GLib = GLib()
        self.mainloop = GLib.MainLoop()
        if run_mainloop:
            threading.Thread(target=self.mainloop.run, daemon=True).start()

        self._debug = debug
        self.bus = dbus.SystemBus()
        adapter = find_adapter(self.bus)
        assert adapter
        self._adapter = adapter

        self._ad_manager = AdvertisingManager(self.bus, self._adapter)
        self._app_manager = ApplicationManager(self.bus, self._adapter)
        self._agent_manager = AgentManager(self.bus)

        self.on_advertising_change: Optional[AdvertsementChangeCallback] = None
        """
        Callback invoked when the advertising status changes or there is an error.
        
        Args:
            bool: The new advertising state
            DBUSException: The exception if there is one. Defaults to None
        """

        self.on_connect: Optional[DeviceEventCallback] = None
        self.on_disconnect: Optional[DeviceEventCallback] = None

        self.bus.add_signal_receiver(
            self._properties_changed,
            dbus_interface=DBUS_PROPERTIES,
            signal_name="PropertiesChanged",
            path_keyword="path",
        )
        self.bus.add_signal_receiver(
            self._interfaces_added,
            dbus_interface=DBUS_OM_IFACE,
            signal_name="InterfacesAdded",
        )

        self._ad: Optional[Advertisement] = None
        self._advertising: bool = False

        self._app: Optional[Application] = None
        self._agent: Optional[Agent] = None

        self.connected = False

    def set_advertisement(self, ad: Advertisement, start: bool = False):
        # If we are advertising, unregister the current advertisement
        self.advertising = False

        self._ad = ad

        if start:
            self.advertising = True

    @property
    def advertising(self):
        return self._advertising

    @advertising.setter
    def advertising(self, state: bool):
        if state is True:
            if self._ad is None:
                raise ValueError(
                    "No advertisement set. Remember to call `set_advertisement` first"
                )

            self._ad_manager.register_advertisement(
                self._ad,
                on_success=self.__advertising_registered,
                on_error=self.__advertising_error,
            )

        elif self._ad:
            self._ad_manager.unregister_advertisement(
                self._ad,
                on_success=self.__advertising_unregistered,
                on_error=self.__advertising_error,
            )

    @property
    def agent(self):
        return self._agent

    @property
    def application(self):
        return self._app

    @application.setter
    def application(self, app: Optional[Application]):
        if app is None:
            if self._app:
                self._app_manager.unregister_application(self._app)
                self._app = None
        else:
            self._app = app
            self._app_manager.register_application(app)

    @agent.setter
    def agent(self, agent: Optional[Agent]):
        if agent is None:
            if self._agent:
                self._agent_manager.unregister_agent(self._agent)
                self._agent = None
        else:
            self._agent = agent
            self._agent_manager.register_agent(self._agent)

    def _set_connected_status(self, status):
        if status == 1:
            self.connected = True
            self.advertising = False

            if self.on_connect:
                self.on_connect("s")
        else:
            self.connected = False
            self.advertising = True

            if self.on_disconnect:
                self.on_disconnect("s")

    def _properties_changed(
        self,
        interface,
        changed,
        invalidated,
        path,
    ):
        if self._debug:
            print("Properties changed")
            print(f"Interface: {interface}")
            print(f"Changed: {changed}")
            print(f"Invalidated: {invalidated}")
            print(f"Path: {path}")
        if interface == DEVICE_INTERFACE:
            if "Connected" in changed:
                self._set_connected_status(changed["Connected"])

    def _interfaces_added(
        self,
        path,
        interfaces,
    ):
        print("Interfaces added")
        print(f"Path: {path}")
        print(f"Interfaces: {interfaces}")
        if DEVICE_INTERFACE in interfaces:
            properties = interfaces[DEVICE_INTERFACE]
            if "Connected" in properties:
                self._set_connected_status(properties["Connected"])

    def __advertising_registered(self):
        self._advertising = True
        if self.on_advertising_change:
            self.on_advertising_change(True, None)

    def __advertising_unregistered(self):
        self._advertising = False
        if self.on_advertising_change:
            self.on_advertising_change(False, None)

    def __advertising_error(self, error):
        if self.on_advertising_change:
            self.on_advertising_change(self._advertising, error)

    def _app_added(self):
        print("Added application")

    def _app_error(self, error):
        print(f"Cannot add application: {error}")

    def _agent_added(self):
        print("Added agent")

    def _agent_error(self, error):
        print(f"Cannot add agent: {error}")
