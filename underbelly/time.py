from loguru import logger
from underbelly import EnvModule
from underbelly.envs import schemas, dbs, intop

from underbelly.envs.modules.intop import Interoperator
from underbelly.envs.modules.dbs import PlaceholderDB
from underbelly.envs.modules.schemas import MetricSchema


class TimeseriesEnv(EnvModule):
    """MetricsModule

    The metrics module sends and recieves metrics to the timeseries database below.

    Args:
        EnvModule ([type]): [description]
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.dependencies = {}
        self.schema = MetricSchema()
        self.db = PlaceholderDB()
        # This is where all of your specific commands go.
        self.intop = Interoperator()
        self.conn = dbs.IConnection()

    def send(self, _metrics: dict):
        self.intop.dispatch(_metrics)
