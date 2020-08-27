from underbelly.envs.utils import *
from underbelly.envs.schemas import Identifier
from underbelly.imports import *


class DBOpsPayload(abc.ABC):
    pass


class IDatabase(abc.ABC):
    """Database Abstract

    Will use to hold general functions and functionality for the updateself.
    
    
    It will also have better features as time progresses. All to speed up the system.
    """

    def initialize(self, info: DBOpsPayload):
        raise NotImplementedError

    def save(self, info: DBOpsPayload):
        raise NotImplementedError

    def save_many(self, info: DBOpsPayload):
        raise NotImplementedError

    def delete(self, info: DBOpsPayload):
        raise NotImplementedError

    def latest(self, info: DBOpsPayload) -> dict:
        raise NotImplementedError

    def latestmany(self, info: DBOpsPayload):
        raise NotImplementedError

    def between(self, info: DBOpsPayload) -> list:
        raise NotImplementedError

    def latestby(self, info: DBOpsPayload) -> dict:
        raise NotImplementedError

    def latestall(self, info: DBOpsPayload):
        raise NotImplementedError

    def count(self, info: DBOpsPayload) -> int:
        raise NotImplementedError

    def deletefirst(self, info: DBOpsPayload):
        raise NotImplementedError

    def get(self, info: DBOpsPayload):
        raise NotImplementedError

    def put(self, info: DBOpsPayload):
        raise NotImplementedError

    def clear(self, info: DBOpsPayload):
        raise NotImplementedError

    def lock(self, info: DBOpsPayload):
        raise NotImplementedError


class PlaceholderDB(IDatabase):
    """Placeholder Database

    A dummy database

    Parameters
    ----------
    IDatabase : type
        Abstract database connection.
    """

    def __init__(self) -> None:
        pass

    def initialize(self, info: DBOpsPayload):
        logger.debug("Initializing command")

    def save(self, info: DBOpsPayload):
        logger.debug("Initializing command")

    def save_many(self, info: DBOpsPayload):
        logger.debug("Initializing command")

    def delete(self, info: DBOpsPayload):
        logger.debug("Initializing command")

    def latest(self, info: DBOpsPayload) -> dict:
        logger.debug("Initializing command")
        return dict()

    def latest_of(self, info: DBOpsPayload) -> list:
        # You get the latest of multiple items.
        # E.g get the latest price for BTC, ETH, LINK will return a list of dicts for each field
        logger.debug("Initializing command")
        return []

    def latest_many(self, info: DBOpsPayload) -> list:
        logger.debug("Initializing command")
        return []

    def latest_of_many(self, info: DBOpsPayload) -> list:
        # You get the last of multiple items.
        # E.g get the latest price for BTC, ETH, LINK will return a list of dicts for each field. 
        logger.debug("Initializing command")
        return []

    def between(self, info: DBOpsPayload) -> list:
        logger.debug("Initializing command")
        return []

    def latestby(self, info: DBOpsPayload) -> dict:
        logger.debug("Initializing command")
        return {}

    def latestall(self, info: DBOpsPayload) -> list:
        logger.debug("Initializing command")
        return []

    def count(self, info: DBOpsPayload) -> int:
        logger.debug("Initializing command")
        return 0

    def deletefirst(self, info: DBOpsPayload):
        logger.debug("Initializing command")

    def get(self, info: DBOpsPayload):
        logger.debug("Initializing command")
        return dict

    def put(self, info: DBOpsPayload):
        logger.debug("Initializing command")

    def clear(self, info: DBOpsPayload):
        logger.debug("Initializing command")

    def lock(self, info: DBOpsPayload):
        logger.debug("Initializing command")