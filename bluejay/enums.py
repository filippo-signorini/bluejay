import enum


class AgentCapability(str, enum.Enum):
    DISPLAY_ONLY = "DisplayOnly"
    DISPLAY_YES_NO = "DisplayYesNo"
    KEYBOARD_ONLY = "KeyboardOnly"
    KEYBOARD_DISPLAY = "KeyboardDisplay"
    NO_INPUT_OUTPUT = "NoInputNoOutput"


class AdType(str, enum.Enum):
    """Advertisement Type"""

    BROADCAST = "broadcast"
    PERIPHERAL = "peripheral"


class Appearance(enum.IntEnum):
    GENERIC_ACCESS_CONTROL = 0x0700
    ACCESS_DOOR = 0x701


class DescriptorFlag(str, enum.Enum):
    READ = "read"
    WRITE = "write"
    ENCRYPT_READ = "encrypt-read"
    ENCRYPT_WRITE = "encrypt-write"
    ENCRYPT_AUTHENTICATED_READ = "encrypt-authenticated-read"
    ENCRYPT_AUTHENTICATED_WRITE = "encrypt-authenticated-write"
    SECURE_READ = "secure-read"
    SECURE_WRITE = "secure-write"
    AUTHORIZE = "authorize"


class CharacteristicFlag(str, enum.Enum):
    BROADCAST = "broadcast"
    READ = "read"
    WRITE_WITHOUT_RESPONSE = "write-without-response"
    WRITE = "write"
    NOTIFY = "notify"
    INDICATE = "indicate"
    AUTHENTICATED_SIGNED_WRITES = "authenticated-signed-writes"
    EXTENDED_PROPERTIES = "extended-properties"
    RELIABLE_WRITE = "reliable_write"
    WRITABLE_AUXILIARIES = "writable-auxiliaries"
    ENCRYPT_READ = "encrypt-read"
    ENCRYPT_WRITE = "encrypt-write"
    ENCRYPT_NOTIFY = "encrypt-notify"
    ENCRYPT_INDICATE = "encrypt-indicate"
    ENCRYPT_AUTHENTICATED_READ = "encrypt-authenticated-read"
    ENCRYPT_AUTHENTICATED_WRITE = "encrypt-authenticated-write"
    ENCRYPT_AUTHENTICATED_NOTIFY = "encrypt-authenticated-notify"
    ENCRYPT_AUTHENTICATED_INDICATE = "encrypt-authenticated-indicate"
    SECURE_READ = "secure-read"
    SECURE_WRITE = "secure-write"
    SECURE_NOTIFY = "secure-notify"
    SECURE_INDICATE = "secure-indicate"
    AUTHORIZE = "authorize"
