from underbelly.envs.utils import *
from underbelly.imports import *
from underbelly.envs.schemas import Identifier
from underbelly.envs.dbs import IPayload, IDatabase, LocalPayload


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

    def initialize(self, info: IPayload):
        logger.debug("Initializing command")

    def heartbeat(self, LocalPayload):
        logger.debug("Initializing command")

    def save(self, info: IPayload):
        logger.debug("Initializing command")

    def save_many(self, info: IPayload):
        logger.debug("Initializing command")

    def delete(self, info: IPayload):
        logger.debug("Initializing command")

    def latest(self, info: IPayload) -> dict:
        logger.debug("Initializing command")
        return dict()

    def latest_of(self, info: IPayload) -> list:
        # You get the latest of multiple items.
        # E.g get the latest price for BTC, ETH, LINK will return a list of dicts for each field
        logger.debug("Initializing command")
        return []

    def latest_many(self, info: IPayload) -> list:
        # Get the latest of a single item.
        logger.debug("Initializing command")
        return []

    def latest_of_many(self, info: IPayload) -> list:
        # You get the last of multiple items.
        # E.g get the latest price for BTC, ETH, LINK will return a list of dicts for each field.
        logger.debug("Initializing command")
        return []

    def between(self, info: IPayload) -> list:
        logger.debug("Initializing command")
        return []

    def latestby(self, info: IPayload) -> dict:
        logger.debug("Initializing command")
        return {}

    def latestall(self, info: IPayload) -> list:
        logger.debug("Initializing command")
        return []

    def count(self, info: IPayload) -> int:
        logger.debug("Initializing command")
        return 0

    def deletefirst(self, info: IPayload):
        logger.debug("Initializing command")

    def get(self, info: IPayload):
        logger.debug("Initializing command")
        return dict

    def put(self, info: IPayload):
        logger.debug("Initializing command")

    def clear(self, info: IPayload):
        logger.debug("Initializing command")

    def lock(self, info: IPayload):
        logger.debug("Initializing command")