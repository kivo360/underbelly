import abc
from underbelly import DataProcessor, DataSchema


class EnvModuleType(abc.ABCMeta):
    """ We use this to check if the proper variables are available after the init function """

    def __call__(cls, *args, **kwargs):
        obj = type.__call__(cls, *args, **kwargs)
        obj._verify_fields()
        return obj


class EnvModule(metaclass=EnvModuleType):

    def __init__(self, *args, **kwargs):
        self.depenencies = {}
        self._base_essentials = {
            "schema": DataSchema, "processor": DataProcessor
        }

    def step(self, *args, **kwargs):
        raise NotImplementedError

    def reset(self):
        raise NotImplementedError

    def render(self):
        raise NotImplementedError

    def __verify_all_inate_types(self):
        dep_len = len(self.depenencies)
        if dep_len == 0: return
        for k, v in self.depenencies.items():
            if k not in self.__dict__:
                raise AttributeError(
                    f"{k} is not in the dependencies. You have to add it."
                )
            if not isinstance(self.__dict__[k], v):

                raise AttributeError(
                    f"{k} is not the right instance type. It should be {v}"
                )

    def __merge_essential_fields(self):
        self._base_essentials.update(self.dependencies)
        self.dependencies = copy.copy(self._base_essentials)

    def _verify_fields(self):
        self.__merge_essential_fields()
        self.__verify_all_inate_types()
