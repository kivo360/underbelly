from underbelly.imports import *
from underbelly.valid import IDependenciesAbstract
from underbelly import IDatabase, ISchema, Interoperator, IConnection


class EnvModule(IDependenciesAbstract, abc.ABC):
    """Env Module

    The environment module is a place where all parts of the system will interact with each other.
    
    The point of rebuilding this time arouond is to accellerate parts of the process and make the system more modular.

    It operates a lot like pytorch. It automatically adds schema and database reference information to connect to other modules inside of the system.
    
    As more modules are attached they recieve reference inside of the subsystem for possible preplanning.
    """
    _dependencies = {
        "db": IDatabase,
        "schema": ISchema,
        'intop': Interoperator,
        'conn': IConnection
    }

    def __init__(self, *args, **kwargs):
        super(EnvModule, self).__init__(*args, **kwargs)

    def step(self, *args, **kwargs):
        raise NotImplementedError

    def reset(self):
        raise NotImplementedError

    def render(self):
        raise NotImplementedError

    def __dependency_injection(self):
        self.intop.attach(self.db, self.schema, self.conn)

    @property
    def database(self) -> IDatabase:
        return self.db

    @property
    def ioper(self) -> Interoperator:
        return self.intop

    def _verify_fields(self):
        super()._verify_fields()

        self.__dependency_injection()
