from uuid import uuid4
from loguru import logger
from underbelly import EnvModule
from underbelly.background import PlaceholderSchema, PlaceholderDB
from underbelly.orders import Trade


class Executor(EnvModule):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.dependencies = {}
        self.schema = PlaceholderSchema()
        self.database = PlaceholderDB()

    def submit(self):
        logger.info("Hello world")