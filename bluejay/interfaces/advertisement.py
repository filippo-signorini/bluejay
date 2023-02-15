import typing

import dbus
import dbus.service

from ..constants import ADVERTISEMENT_INTERFACE, DBUS_PROPERTIES
from ..enums import AdType
from ..exceptions import InvalidArgsException
from ..utils import is_empty_array, is_empty_dict


class Advertisement(dbus.service.Object):
    """Base Advertisement class"""

    # PATH_BASE = "/org/bluez/example/advertisement"

    def __init__(
        self,
        bus: dbus.SystemBus,
        path: str,
        index: int,
        ad_type: AdType,
    ):
        self.path = f"{path}/advertisement{index}"
        self.bus = bus
        self.ad_type: str = ad_type.value
        """
        Determines the type of advertising packet requested.

        Possible values: `broadcast` or `peripheral`.
        """

        self.service_uuids: typing.Optional[list[str]] = None
        """
        List of UUIDs to include in the `Service UUID` field of the
        `Advertising Data`.
        """

        self.manufacturer_data: typing.Optional[dict[int, typing.Any]] = None
        """
        Manufacturer Data fields to include in the Advertising Data.
        Keys are the manufacturer ID to associate with the data.
        """

        self.solicit_uuids: typing.Optional[list[str]] = None
        """
        Array of UUIDs to include in `Service Solicitation` Advertisement Data.
        """

        self.service_data: typing.Optional[dict] = None
        """
        Service Data elements to include. The keys are the UUID to associate
        with the data.
        """

        self.data: typing.Optional[dict[int, list[int]]] = None
        """
        *Experimental*

        Advertising Type to include in the Advertising Data. Key is the
        advertising type and value is the data as byte array.

        Note: Types already handled by other properties shall not be used.

        Possible values:
            <type> <byte array>
            ...

        Example:
            <Transport Discovery> <Organization Flags...>
            0x26                  0x01          0x01...
        """

        self.discoverable: typing.Optional[bool] = None
        """
        *Experimental*

        Advertise as general discoverable. When present this will override
        adapter Discoverable property.

        Note: This property shall not be set when Type is set to 'broadcast'.
        """

        self.discoverable_timeout: typing.Optional[int] = None
        """
        The discoverable timeout in seconds. A value of zero means that the
        timeout is disabled and it will stay in discoverable/limited mode
        forever.

        Note: This property shall not be set when Type is set to 'broadcast'.
        """

        self.includes: typing.Optional[list[str]] = None
        """
        List of features to be included in the advertising packet.

        Possibile values: as found on `LEAdvertisingManager.SupportedIncludes`.
        """

        self.local_name: typing.Optional[str] = None
        """
        Local name to be used in the advertising report. If the string is
        too big to fit into the packet it will be truncated.

        If this proeprty is available `local-name` cannot be present in the
        includes.
        """

        self.appearance: typing.Optional[int] = None
        """
        Apperance to be used in the advertising report.

        Possible values: as found on `GAP Service`.
        """

        self.duration: typing.Optional[int] = None
        """
        Rotation duration of the advertisement in seconds. If there are other
        applications advertising no duration is set.
        The default is 2 seconds.
        """

        self.timeout: typing.Optional[int] = None
        """
        Timeout of the advertisement in seconds. This defines the lifetime
        of the advertisement.
        """

        self.secondary_channel: typing.Optional[str] = None
        """
        *Experimental*

        Secondary channel to be used. Primary channel is always set to `1M`
        except when `Coded` is set.

        Possilbe values: `1M` (default), `2M`, `Coded`
        """

        self.min_interval: typing.Optional[int] = None
        """
        *Experimental*

        Minimum advertising interval to be used by the advertising set,
        in milliseconds. Acceptable values are in the range [20ms, 10.485s].
        If the provided `MinInterval` is larget than the provided
        `MaxInterval`, the registration will return failure.
        """

        self.max_interval: typing.Optional[int] = None
        """
        *Experimental*

        Maximum advertising interval to be used by the advertising set,
        in milliseconds. Acceptable values are in the range [20ms, 10.485s].
        If the provided `MinInterval` is larger than the provided
        `MaxInterval`, the registration will return failure.
        """

        self.tx_power: typing.Optional[int] = None
        """
        *Experimental*

        Requested transmission power of this advertising set.
        The provided value is used only if the `CanSetTxPower` feature
        is enabled on the `Advertising Manager`. The provided value must be
        in range [-127, +20], where units are in dBm.
        """

        super().__init__(bus, self.path)

    def get_properties(self):
        properties = {"Type": dbus.String(self.ad_type)}
        if not is_empty_array(self.service_uuids):
            properties["ServiceUUIDs"] = dbus.Array(self.service_uuids, signature="s")
        if not is_empty_dict(self.manufacturer_data):
            properties["ManufacturerData"] = dbus.Dictionary(
                self.manufacturer_data, signature="qv"
            )
        if not is_empty_array(self.solicit_uuids):
            properties["SolicitUUIDs"] = dbus.Array(self.solicit_uuids, signature="s")
        if not is_empty_dict(self.service_data):
            properties["ServiceData"] = dbus.Dictionary(
                self.service_data, signature="sv"
            )
        if not is_empty_dict(self.data):
            properties["Data"] = dbus.Dictionary(self.data, signature="yv")
        if self.discoverable:
            properties["Discoverable"] = dbus.Boolean(True)
        if self.discoverable_timeout:
            properties["DiscoverableTimeout"] = dbus.UInt16(self.discoverable_timeout)
        if not is_empty_array(self.includes):
            properties["Includes"] = dbus.Array(self.includes, signature="s")
        if self.local_name:
            properties["LocalName"] = dbus.String(self.local_name)
        if self.appearance:
            properties["Appearance"] = dbus.UInt16(self.appearance)
        if self.duration:
            properties["Duration"] = dbus.UInt16(self.duration)
        if self.timeout:
            properties["Timeout"] = dbus.UInt16(self.timeout)
        if self.secondary_channel:
            properties["SecondaryChannel"] = dbus.String(self.secondary_channel)
        if self.min_interval:
            properties["MinInterval"] = dbus.UInt32(self.min_interval)
        if self.max_interval:
            properties["MaxInterval"] = dbus.UInt32(self.max_interval)
        if self.tx_power:
            properties["TxPower"] = dbus.Int16(self.tx_power)
        return {ADVERTISEMENT_INTERFACE: properties}

    def get_path(self):
        return dbus.ObjectPath(self.path)

    def add_service_uuid(self, uuid: str):
        if not self.service_uuids:
            self.service_uuids = []
        self.service_uuids.append(uuid)

    def add_solicit_uuid(self, uuid: str):
        if not self.solicit_uuids:
            self.solicit_uuids = []
        self.solicit_uuids.append(uuid)

    def add_manufacturer_data(self, manuf_code: int, data):
        if not self.manufacturer_data:
            self.manufacturer_data = {}
        self.manufacturer_data[manuf_code] = dbus.Array(data, signature="y")

    def add_service_data(self, uuid: str, data):
        if not self.service_data:
            self.service_data = {}
        self.service_data[uuid] = dbus.Array(data, signature="y")

    def add_data(self, ad_type: int, data):
        if not self.data:
            self.data = {}
        self.data[ad_type] = dbus.Array(data, signature="y")

    @dbus.service.method(DBUS_PROPERTIES, in_signature="s", out_signature="a{sv}")
    def GetAll(
        self,
        interface: dbus.Interface,
    ):  # pylint: disable=invalid-name
        if interface != ADVERTISEMENT_INTERFACE:
            raise InvalidArgsException()
        return self.get_properties()[ADVERTISEMENT_INTERFACE]
