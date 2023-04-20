from typing import Any, Callable, Optional, TypeVar, Union

import dbus.mainloop.glib
from gi.repository import GLib as _GLib  # type: ignore

_T = TypeVar("_T")


class GLib:
    @staticmethod
    def MainLoop():
        return MainLoop()

    @staticmethod
    def timeout_add(
        interval: int,
        function: Union[Callable[[_T], Any], Callable[[], Any]],
        data: Optional[_T] = None,
    ) -> int:
        """
        Sets a function to be called at regular intervals (after `interval`)
        until it returns `False` or is cancelled with `source_remove`

        #### Args:
            `interval`: Time between calls to the function, in milliseconds.
            `function`: Function to call.
            `data`: Data to pass to funciton.

        #### Returns:
            `int`: The id of the event source used to cancel the interval.

        If you want to have a timer in the "seconds" range and do not care
        about the exact time of the first call of the timer use
        `timeout_add_seconds()`

        Note that the first call of the timer may not be precise for timeouts
        of one second. If you need finer precision and have such a timeout,
        you want to use `timeout_add()` instead.
        """

        if data is None:
            return _GLib.timeout_add(interval, function)
        else:
            return _GLib.timeout_add(interval, function, data)

    @staticmethod
    def timeout_add_seconds(
        interval: int,
        function: Union[Callable[[_T], Any], Callable[[], Any]],
        data: Optional[_T] = None,
    ) -> int:
        """
        Sets a function to be called at regular intervals (after `interval`)
        until it returns `False` or is cancelled with `source_remove`

        #### Args:
            `interval`: Time between calls to the function, in seconds.
            `function`: Function to call.
            `data`: Data to pass to funciton.

        #### Returns:
            `int`: The id of the event source used to cancel the interval.

        Note that the first call of the timer may not be precise for timeouts
        of one second. If you need finer precision and have such a timeout,
        you want to use `timeout_add()` instead.
        """

        if data is None:
            return _GLib.timeout_add_seconds(interval, function)
        else:
            return _GLib.timeout_add_seconds(interval, function, data)

    @staticmethod
    def source_remove(id: Optional[int]) -> bool:
        """
        Cancels the timeout with the given ID, returned from the functions
        `timeout_add()` and `timeout_add_seconds()`

        #### Args:
            `id`: ID of the source to remove

        #### Returns:
            `bool`: Returns `True` if the timeout was removed, false otherwise
        """
        if id is not None:
            if _GLib.MainContext.default().find_source_by_id(id) is not None:
                _GLib.source_remove(id)
                return True

        return False


class MainLoop:
    def __init__(self):
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        self._mainloop = _GLib.MainLoop()

    def run(self):
        self._mainloop.run()

    def quit(self):
        self._mainloop.quit()
