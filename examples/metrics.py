from loguru import logger
from underbelly import EnvModule
from underbelly.envs import schemas, dbs, intop


class Metrics(EnvModule):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.dependencies = {}
        self.schema = schemas.MetricSchema()
        self.db = dbs.PlaceholderDB()
        self.intop = intop.Interoperator()
        self.conn = dbs.IConnection()

    def send(self, _metrics: dict):
        self.intop.dispatch(_metrics)


if __name__ == "__main__":
    meter = Metrics()
    meter.send({"shit": "stick"})