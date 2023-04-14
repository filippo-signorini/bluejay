from typing import Callable, Optional

import dbus.mainloop.glib
from gi.repository import GLib as _GLib  # type: ignore


class GLib:
    @staticmethod
    def MainLoop():
        return MainLoop()

    @staticmethod
    def timeout_add(interval_milli: int, cb: Callable) -> int:
        return _GLib.timeout_add(interval_milli, cb)

    @staticmethod
    def source_remove(id: Optional[int]):
        if id is not None:
            _GLib.source_remove(id)


class MainLoop:
    def __init__(self):
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        self._mainloop = _GLib.MainLoop()

    def run(self):
        self._mainloop.run()

    def quit(self):
        self._mainloop.quit()
