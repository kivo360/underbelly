# Orders - Python Design

The base of the python design is the `Order` to get a good idea of what that looks like, I'm going to sample from tensortrades order mechanism:

**I've decided to move all of the existing sample code into to the bottom**

We know how to formulate a trade. We push that trade into a system that proxy's the broker connection. Ideally, that should be the location we submit the trade:

For trades we have to have some interaction between our internal exchange and outside. It's recommended to have a broker as a proxy.

Exchange -> Broker -> Executor

We already know what we'll do for the exchange, though we'd need to fundamentally define what we're doing inside of executor.

**Broker:**
* Keeps track of the orders internally.
* Sends commands to the `Executor`.
    * Submitting an order
    * Getting the status of an order.
    * Cancelling an order.
    * Handles possible errors from talking to the exchange.
    * Adds a retry system with exponential backoff retry.
    * Gets stats about trades over a given window.
    * Slippage statistics
    * Average time to fill trades.


## Example Uses: Trade Broker Interaction

### Submitting A Trade

```python
user_params = { ... }
trade = Trade(...) # Define a trade (we already know how to do this.)
broker = Broker(...) # Send the trade to the broker
broker.group_settings(**user_params)
broker.submit(trade)
```

### Getting Trades - For Current User

#### Open

```python
broker_params = {
    "status": "OPEN"
}
group_params = { ... }
time_params = {
    "time_type": "relative", # Check by the relative time.
    "latest_group": True # Get the latest of each group.
}
broker = Broker(...) # Send the trade to the broker
broker.time_settings(**time_params) # Explain how to deal with time
broker.group_settings(**group_params) # group by these settings
open_trades = broker.load(**broker_params)
```

#### Closed

```python
broker_params = {
    "status": "CLOSED"
}
group_params = { ... }
time_params = {
    "time_type": "relative", # Check by the relative time.
    "latest_group": True # Get the latest of each group.
}
broker = Broker(...) # Send the trade to the broker
broker.time_settings(**time_params) # Explain how to deal with time
broker.group_settings(**group_params) # group by these settings
closed_trades = broker.load(**broker_params)
```

#### Pending

```python
broker_params = {
    "status": "PENDING"
}
group_params = { ... }
time_params = {
    "time_type": "relative", # Check by the relative time.
    "latest_group": True # Get the latest of each group.
}
broker = Broker(...) # Send the trade to the broker
broker.time_settings(**time_params) # Explain how to deal with time
broker.group_settings(**group_params) # group by these settings
pending_trades = broker.load(**broker_params)
```

#### Cancelled

```python
broker_params = {
    "status": "CANECELLED"
}
group_params = { ... }
time_params = {
    "time_type": "relative", # Check by the relative time.
    "latest_group": True # Get the latest of each group.
}
broker = Broker(...) # Send the trade to the broker
broker.time_settings(**time_params) # Explain how to deal with time
broker.group_settings(**group_params) # group by these settings
cancelled_trades = broker.load(**broker_params) # 
```

### Checking Trades

When we get the trades from the load function it would have an id we can use to identify everything inside of the Executor. For example, after calling all of the trade information:

```python
open_trades = broker.load(**broker_params)
for trade in open_trades:
    # Each of these loaded trades will have an executor_id inside of it from the executor.
    # If they don't have an executor_id, it won't check.
    broker.check_trade(trade)
```

```python
def check_trade(self, trade: Trade):
    """ Checks the trade status from the executor. """
    if not trade.is_trade: return 
    executor_id: str = trade.executor_id
    status: Status = self.executor.get_status(executor_id) # Get the status from the exchange
    
    # We manage the errors here
    self.manage_error(status)
    # The status class from the executor will have the status of the trade
    # Check if the trade status is different from the trade we entered into
    if self.is_different(status, trade):
        self.update_state(status)
```

As you see `check_trade` doesn't have parameters for identifying the executor. The trade object in the parameter also has specific parameters to give us some idea which detailed executor we should be using.

```python
def get_status(self, executor_id:str):
    api_keys = self.get_api_key(executor_id) # we'd reach out to the API key first.
    status_dict: dict = self.api.pull_status(api_keys, executor_id)
    status = Status().cast(**status_dict)
    return status
```