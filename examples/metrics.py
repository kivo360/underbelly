from underbelly.imports import *
from underbelly import EnvModule
from underbelly.envs import db
from underbelly.envs.models import *
from underbelly.envs.modules.opts import Operators, MetricOperator
from underbelly.envs.modules.db import PlaceholderDB
from underbelly.envs.modules import MetricSchema


class Metrics(EnvModule):
    """MetricsModule

    The metrics module sends and recieves metrics to the timeseries database below.

    Args:
        EnvModule ([type]): [description]
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.dependencies = {}
        self.schema = MetricSchema()
        self.conn = IConnection()
        self.db = PlaceholderDB(self.conn)
        # This is where all of your specific commands go.
        self.opts = MetricOperator()

    def report(self, _metrics: IPayload):
        self.opts.dispatch(_metrics)


if __name__ == "__main__":
    current_monitor = Metrics()
    while True:
        payload = MetricsPayload(
            entity="rewards",
            command_type=CommandTypes.RECORD,
            labels=dict(hello="world"),
            values=dict(price=random.uniform(0, 1000))
        )
        current_monitor.report(payload)