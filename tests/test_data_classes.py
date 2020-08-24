"""
Test Data Classes

The data classes will be crucial in making sure we don't accidentally nuke the system. 

If anything is wrong with how we're accessing the exchange we'll have extremely consistent information explaining how it it's broken.

This will be absolutely critical in making sure this system doesn't blow up, and tat we can send proper logs into the system.
"""
from underbelly.orders import TradeCaster


def test_extract_trade():
    trade_caster = TradeCaster()

    # No user_id
