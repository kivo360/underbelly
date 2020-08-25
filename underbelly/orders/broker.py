from uuid import uuid4
from loguru import logger
from underbelly import EnvModule
from underbelly.background import PlaceholderSchema, PlaceholderDB
from underbelly.orders import Trade, executor


class Broker(EnvModule):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.dependencies = {}
        self.schema = PlaceholderSchema()
        self.database = PlaceholderDB()
        self.executor = executor.Executor()

    def set_identifiers(
        self,
        userid: str,
        episode: str,
        exchange: str = "backtest",
        live: bool = False
    ):
        self.schema.set_identifiers(
            userid=userid, episode=episode, exchange=exchange, live=live
        )


    def submit(self, trade: Trade) -> Trade:
        if trade.is_order:
            raise ValueError(
                "You can't submit a trade that's already been submitted."
            )
        trade.orderid = uuid4().hex
        self.executor.submit()
        return trade

    def check(self):
        pass

    def cancel(self):
        pass

    def orders(self):
        pass

    def openned(self):
        pass

    def synchronized(self):
        pass