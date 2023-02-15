import threading
from typing import Callable, Optional

import dbus
import dbus.service

from .constants import (
    ADVERTISING_MANAGER_INTERFACE,
    AGENT_MANAGER_INTERFACE,
    BLUEZ_NAMESPACE,
    BLUEZ_SERVICE_NAME,
    DBUS_OM_IFACE,
    DBUS_PROPERTIES,
    DEVICE_INTERFACE,
    GATT_MANAGER_INTERFACE,
)
from .glib import GLib
from .interfaces.advertisement import Advertisement
from .interfaces.agent import Agent
from .interfaces.gatt import Application
from .types import DBUSErrorCallback, DeviceEventCallback, NoneCallback
from .utils import find_adapter


class BLEManager:
    def __init__(self, base_path: str, debug=False):
        self.base_path = base_path
        self.GLib = GLib()
        self.mainloop = GLib.MainLoop()
        threading.Thread(target=self.mainloop.run, daemon=True).start()

        self._debug = debug
        self.bus = dbus.SystemBus()
        adapter = find_adapter(self.bus)
        assert adapter
        self._adapter = adapter

        self._ad_manager = _AdManager(self.bus, self._adapter)
        self._app_manager = _AppManager(self.bus, self._adapter)
        self._agent_manager = _AgentManager(self.bus)

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

    def set_advertisement(self, ad: Advertisement, start_ad: bool = False):
        # If we are advertising, unregister the current advertisement
        self.advertising = False

        self._ad = ad

        if start_ad:
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

            self._ad_manager.register_advertisement(self._ad)
            self._advertising = True

        elif self._ad:
            self._ad_manager.unregister_advertisement(self._ad)
            self._advertising = False

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

    def _adv_added(self):
        print("Added advertisement")

    def _adv_error(self, error):
        print(f"Cannot add advertisement: {error}")
        self.advertisement = None

    def _app_added(self):
        print("Added application")

    def _app_error(self, error):
        print(f"Cannot add application: {error}")

    def _agent_added(self):
        print("Added agent")

    def _agent_error(self, error):
        print(f"Cannot add agent: {error}")


class _AdManager:
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
        print(f"Registering advertisement {ad.get_path()}")
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


class _AppManager:
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


class _AgentManager:
    def __init__(self, bus: dbus.SystemBus):
        self._interface = dbus.Interface(
            bus.get_object(BLUEZ_SERVICE_NAME, BLUEZ_NAMESPACE),
            AGENT_MANAGER_INTERFACE,
        )

    def register_agent(
        self,
        agent: Agent,
        on_success: Optional[NoneCallback] = None,
        on_error: Optional[DBUSErrorCallback] = None,
    ):
        self._interface.RegisterAgent(
            agent.get_path(),
            agent.capability,
            reply_handler=on_success,
            error_handler=on_error,
        )
        self._request_default_agent(agent, on_success, on_error)

    def _request_default_agent(
        self,
        agent: Agent,
        on_success: Optional[NoneCallback] = None,
        on_error: Optional[DBUSErrorCallback] = None,
    ):
        self._interface.RequestDefaultAgent(
            agent.get_path(),
            reply_handler=on_success,
            error_handler=on_error,
        )

    def unregister_agent(
        self,
        agent: Agent,
        on_success: Optional[NoneCallback] = None,
        on_error: Optional[DBUSErrorCallback] = None,
    ):
        self._interface.UnregisterAgent(
            agent.get_path(),
            reply_handler=on_success,
            error_handler=on_error,
        )
