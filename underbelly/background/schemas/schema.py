import abc


class DataSchema(abc.ABC):

    def set_identifiers(self, **kwargs):
        raise NotImplementedError