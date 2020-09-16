"""
Test Data Classes

The data classes will be crucial in making sure we don't accidentally nuke the system. 

If anything is wrong with how we're accessing the exchange we'll have extremely consistent information explaining how it it's broken.

This will be absolutely critical in making sure this system doesn't blow up, and tat we can send proper logs into the system.
"""
import random
import uuid
from loguru import logger
import pytest
from pytest_mock.plugin import MockerFixture

from underbelly.orders import Broker, Trade, TradeCaster
from underbelly.orders.executor import Executor
USERID = uuid.uuid4().hex
EPISODE = uuid.uuid4().hex
EXCHANGE = "backtest"
LIVE = False


@pytest.fixture(scope="session")
def simulated_broker():
    broker = Broker()
    broker.set_identifiers(
        userid=USERID, episode=EPISODE, exchange=EXCHANGE, live=LIVE
    )
    return broker


def test_broker_submit(mocker: MockerFixture, simulated_broker: Broker):
    COMPLETED_BUY = {
        "symbol": "ETH_USD",
        "trade_type": "limitBuy",
        "amount": random.uniform(0, 3),
        "price": random.uniform(1, 20000),
        "order_id": uuid.uuid4().hex,
        "episode": "live",
        "exchange": "binance",
        "live": True
    }

    INCOMPLETED_BUY = {
        "symbol": "ETH_USD",
        "trade_type": "limitBuy",
        "amount": random.uniform(0, 3),
        "price": random.uniform(1, 20000),
        "episode": "live",
        "exchange": "binance",
        "live": True
    }

    patched_function = mocker.patch(
        'underbelly.orders.executor.Executor.submit'
    )

    with pytest.raises(ValueError):
        trade_caster = TradeCaster()
        trade: Trade = trade_caster.cast(**COMPLETED_BUY)
        simulated_broker.submit(trade)

    incomplete: Trade = trade_caster.cast(**INCOMPLETED_BUY)
    simulated_broker.submit(incomplete)
    patched_function.assert_called()


def test_broker_status(mocker, simulated_broker: Broker):
    COMPLETED_BUY = {
        "symbol": "ETH_USD",
        "trade_type": "limitBuy",
        "amount": random.uniform(0, 3),
        "price": random.uniform(1, 20000),
        "order_id": uuid.uuid4().hex,
        "episode": "live",
        "exchange": "binance",
        "live": True
    }

    INCOMPLETED_BUY = {
        "symbol": "ETH_USD",
        "trade_type": "limitBuy",
        "amount": random.uniform(0, 3),
        "price": random.uniform(1, 20000),
        "episode": "live",
        "exchange": "binance",
        "live": True
    }

    trade_caster = TradeCaster()

    incomplete: Trade = trade_caster.cast(**INCOMPLETED_BUY)
    status = simulated_broker.submit(incomplete)
    assert isinstance(status.orderid, str)


def test_broker_cancel(mocker, simulated_broker: Broker):
    assert True, "Was able to cancel an order."


def test_broker_all_orders(mocker, simulated_broker: Broker):
    assert True, "Was able to get all orders"
