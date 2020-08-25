from loguru import logger
from underbelly.background.schemas import DataSchema


class PlaceholderSchema(DataSchema):

    def __init__(self) -> None:
        pass

    def set_identifiers(self, **kwargs):
        logger.info(f"Setting identifier: {kwargs}")