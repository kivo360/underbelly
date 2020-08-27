from enum import Enum
from underbelly.imports import *
from underbelly.envs.utils import *


class CommandTypes(Enum):
    CREATE = 1
    READ = 2
    UPDATE = 3
    DELETE = 4
    LOCAL = 5


class ConnectionTypes(Enum):
    REDIS = 1
    QUERYENGINE = 2


class IConnection(base_model, abc.ABC):
    conn_type: ConnectionTypes = ConnectionTypes.REDIS
    host: str = "localhost"
    port: int = 6739
    secure: bool = False


class BasePayload(base_model, abc.ABC):
    entity: str
    command_type: CommandTypes = CommandTypes.CREATE


class LocalPayload(BasePayload):
    # A payload to ask the local system what's locally there.
    command_type = CommandTypes.LOCAL
    identity_id: str
    question: dict


class IPayload(BasePayload):
    command_type: CommandTypes = CommandTypes.CREATE
    identity: dict
    defined: Optional[AnyDict] = {}


__all__ = ['IPayload', 'CommandTypes', 'IConnection', 'LocalPayload']