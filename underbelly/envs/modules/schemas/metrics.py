from underbelly.envs.modules.schemas import *
from underbelly.envs.utils import *
from underbelly.imports import *


class MetricSchema(ISchema):
    is_predefined = False

    def __init__(
        self,
        entity: Optional[str] = None,
        depenencies: Optional[AnyDict] = None,
        *args,
        **kwargs
    ) -> None:
        super().__init__(entity, depenencies, *args, **kwargs)
        self.entity = "metrics"
        self.identitier = EpisodeIdentifier()
        self.is_watch = True

    def internal_info(self) -> dict:
        pred = None
        if self.predefined is not None:
            pred = self.predefined.definition()
        return {
            "name": self.entity,
            "identity": self.identitier.definition(),
            "predefined": pred,
            'is_watched': self.is_watch
        }

    def __initialize_internal_system(self):
        logger.debug(
            "Sending information about the schema to the lower-level system."
        )

    def _post_init_hooks(self):
        super()._post_init_hooks()
        self.__initialize_internal_system()
        # logger.debug("Checking that we have all of the schema objects.")


if __name__ == "__main__":
    MetricSchema()