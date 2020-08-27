from underbelly import EnvModule
from underbelly.envs import schemas


class Metrics(EnvModule):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.dependencies = {}
        self.schema = schemas.MetricSchema()
        self.database = ub.PlaceholderDB()


if __name__ == "__main__":
    Metrics()