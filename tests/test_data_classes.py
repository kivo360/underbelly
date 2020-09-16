"""
Test Data Classes

The data classes will be crucial in making sure we don't accidentally nuke the system. 

If anything is wrong with how we're accessing the exchange we'll have extremely consistent information explaining how it it's broken.

This will be absolutely critical in making sure this system doesn't blow up, and tat we can send proper logs into the system.
"""
import uuid
import pytest
import random
from underbelly.orders import TradeCaster, Trade


def test_minimum_buy():
    MINIMUM_BUY = {
        "symbol": "ETH_USD",
        "trade_type": "limitBuy",
        "amount": 0.5,
        "price": 30.0,
    }
    trade_caster = TradeCaster()
    assert trade_caster is not None, "Tradecaster failled for some reason."
    with pytest.raises(AttributeError):
        trade_caster.cast()
    trade = trade_caster.cast(**MINIMUM_BUY)
    assert trade is not None, "For some reason the trade is none."
    assert isinstance(trade, Trade), "The trade is not the right kind."
    assert not trade.is_order(), "We have an order id for some reason."
    assert trade.is_pair(), "ERROR: This is not a pair."
    assert trade.is_buy, "This should be a buy."
    assert not trade.is_sell, "This should not be a sell."
    assert trade.is_backtest(), "This is not a backtest"


def test_existing_trade():
    MINIMUM_BUY = {
        "symbol": "ETH_USD",
        "trade_type": "limitBuy",
        "amount": random.uniform(0, 3),
        "price": random.uniform(1, 20000),
        "order_id": uuid.uuid4().hex
    }
    trade_caster = TradeCaster()
    assert trade_caster is not None, "Tradecaster failled for some reason."
    with pytest.raises(AttributeError):
        trade_caster.cast()
    trade = trade_caster.cast(**MINIMUM_BUY)
    assert trade is not None, "For some reason the trade is none."
    assert isinstance(trade, Trade), "The trade is not the right kind."
    assert trade.is_order(), "We have an order id for some reason."
    assert trade.is_pair(), "ERROR: This is not a pair."
    assert trade.is_buy, "This should be a buy."
    assert not trade.is_sell, "This should not be a sell."
    assert trade.is_backtest(), "This is not a backtest"


def test_existing_live():
    MINIMUM_BUY = {
        "symbol": "ETH_USD",
        "trade_type": "limitBuy",
        "amount": random.uniform(0, 3),
        "price": random.uniform(1, 20000),
        "order_id": uuid.uuid4().hex,
        "episode": "live",
        "exchange": "binance",
        "live": True
    }
    trade_caster = TradeCaster()
    assert trade_caster is not None, "Tradecaster failled for some reason."
    with pytest.raises(AttributeError):
        trade_caster.cast()
    trade = trade_caster.cast(**MINIMUM_BUY)
    assert trade is not None, "For some reason the trade is none."
    assert isinstance(trade, Trade), "The trade is not the right kind."
    assert trade.is_order(), "We have an order id for some reason."
    assert trade.is_pair(), "ERROR: This is not a pair."
    assert trade.is_buy, "This should be a buy."
    assert not trade.is_sell, "This should not be a sell."
    assert not trade.is_backtest(), "This is not a backtest"