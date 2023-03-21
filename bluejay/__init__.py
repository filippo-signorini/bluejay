try:
    from bluejay.interfaces.advertisement import Advertisement
except ImportError:
    from .interfaces.advertisement import Advertisement

try:
    from bluejay.interfaces.agent import Agent
except ImportError:
    from .interfaces.agent import Agent

try:
    from bluejay.interfaces.gatt import Application, Characteristic, Descriptor, Service
except ImportError:
    from .interfaces.gatt import Application, Characteristic, Descriptor, Service

try:
    from bluejay.managers.ble_manager import BLEManager
except ImportError:

    from .managers.ble_manager import BLEManager
