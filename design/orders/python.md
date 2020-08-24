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
trade = Trade(...) # Define a trade (we already know how to do this.)
broker = Broker(...) # Send the trade to the broker
broker.submit(trade)
```

### Getting Open Trades - For current user

```python
broker_params = {
    "status": "OPEN"
}
user_params = { ... }
broker = Broker(...) # Send the trade to the broker
broker.settings(**user_params)
open_trades = broker.load(**broker_params)
```


```python
broker_params = {
    "status": "CLOSED"
}
user_params = { ... }
broker = Broker(...) # Send the trade to the broker
broker.settings(**user_params)
closed_trades = broker.load(**broker_params)
```

```python
broker_params = {
    "status": "PENDING"
}
user_params = { ... }
broker = Broker(...) # Send the trade to the broker
broker.settings(**user_params)
closed_trades = broker.load(**broker_params)
```

```python
broker_params = {
    "status": "CANECELLED"
}
user_params = { ... }
broker = Broker(...) # Send the trade to the broker
broker.settings(**user_params)
closed_trades = broker.load(**broker_params)
```