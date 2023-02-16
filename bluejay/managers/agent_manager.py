from typing import Optional

import dbus

from ..constants import AGENT_MANAGER_INTERFACE, BLUEZ_NAMESPACE, BLUEZ_SERVICE_NAME
from ..interfaces.agent import Agent
from ..types import DBUSErrorCallback, NoneCallback


class AgentManager:
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
