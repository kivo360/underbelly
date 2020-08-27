from underbelly.envs import *
from underbelly.envs.modules.dbs import PlaceholderDB
from underbelly.envs.modules.dbs.core import IDatabase
from underbelly.envs.modules.dbs.datamods import *
from underbelly.envs.modules.schemas import MetricSchema
from underbelly.envs.utils import *
from underbelly.imports import *


class _Interopt(base_model):
    db: Optional[IDatabase] = None
    skem: Optional[ISchema] = None
    conn: Optional[IConnection] = None

    class Config:
        arbitrary_types_allowed = True

    def is_none(self) -> bool:
        z = lambda x: x is None
        b = list(filter(z, list(self.__values__)))
        return b == 0


class Interoperator(abc.ABC, metaclass=VerificationType):
    optenv: Optional[_Interopt] = None

    def attach(self, db: IDatabase, schema: ISchema, conn: IConnection):
        self.optenv = _Interopt()
        self.optenv.db = db
        self.optenv.skem = schema
        self.optenv.conn = conn
        self._verify_fields()

    def connect(self):
        if self.optenv.is_none():
            raise AttributeError("Not all fields we entered.")
        logger.success("All values are there calling the db.connect function!")

    def dispatch(self, data: dict):
        logger.warning(data)

    def reset(self):
        self.connect()

    def _verify_fields(self):
        if self.optenv is not None:
            self.reset()


__all__ = ['Interoperator']

if __name__ == "__main__":

    wrapped = Interoperator()
    wrapped.attach(
        db=PlaceholderDB(),
        schema=MetricSchema(),
        conn=IConnection(),
    )
