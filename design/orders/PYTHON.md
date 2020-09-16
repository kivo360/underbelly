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

broker.find_params(**user_params)
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
broker.find_params(**group_params) # group by these settings
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
broker.find_params(**group_params) # group by these settings
closed_trades = broker.load(**broker_params)
```


### Checking Trades

When we get the trades from the load function it would have an id we can use to identify everything inside of the Executor. For example, after calling all of the trade information:

```python
open_trades = broker.load(**broker_params)
for trade in open_trades:
    # Each of these loaded trades will have an order_id inside of it from the executor.
    # If they don't have an order_id, it won't check.
    broker.check_trade(trade)
```

```python
def check_trade(self, trade: Trade):
    """ Checks the trade status from the executor. """
    if not trade.is_order_id: return 
    order_id: str = trade.order_id
    status: Status = self.executor.get_status(order_id) # Get the status from the exchange
    # We manage the errors here
    # We'd also provision the task to run again.
    self.manage_error(status)
    # The status class from the executor will have the status of the trade
    # Check if the trade status is different from the trade we entered into
    if self.is_different(status, trade):
        self.update_state(status)
```

As you see `check_trade` doesn't have parameters for identifying the executor. The trade object in the parameter has specific parameters to give us some idea which detailed executor we should be using.

We can then use the `get_status` method to pull information from the exchange.

**Note:**

In real life pull_status the API class will create a standard status object. We won't have to cast in real life.

```python
def get_status(self, order_id:str):
    api_keys = self.get_api_key(order_id) # we'd reach out to the API key first.
    status_dict: dict = self.api.pull_status(api_keys, order_id)
    status = Status().cast(**status_dict)
    return status
```

In real life, the get status method would likely be an interface. The exact details would vary between each specific implentation detail. We'd just know the inputs and outputs.

```python
def get_status(self, order_id:str) -> Status:
    raise NotImplementedError("Get status not implemented")
```


Given what I know I think it would be possible to create a set of interface classes at the very least. From there on, we can produce the specific version of what we'd need.


It would look like the following:


```python
class Executor(abc.ABC):
    def __init__(self, api:ExternalAPI, creds:ICredentials, validator: IValidation):
        # This is the library that will give us direct access to the API and will return the information in the formatting we want.
        # Eventually it should also store the trading pairs inside of it for validation purposes.
        self.api = api
        self.credentials = creds
        self.validation = validator
    
    def set_credentials(self, user_creds:UserCreds):
        # Sets the credentials. This should run the following steps:
        # Check if we've created the user
        # Create the user if they don't exist
        self.credentials.link(user_creds)
    
    def get_api_key(self, user_id:str, exchange:str):
        """ Should return a user credentials object """
        raise NotImplementedError("You need to have a way to get api keys for the user/exchange.")

    def submit(self, trade:Trade):
        # Submit the trade to the trade execution company
        raise NotImplementedError("You need to have a way to cancel the trades you have.")
    
    def status(self, trade:Trade):
        raise NotImplementedError("You need to have a specific way to get the status.")
    
    def cancel(self, trade:Trade):
        raise NotImplementedError("You need to have a way to cancel the trades you have.")

    def orders(self, user:UserInfo):
        """ Gets all of the user's orders."""
        raise NotImplementedError("You need to have a way to get all of the orders by user information.")
    
    def balance_history(self, user:UserInfo):
        raise NotImplementedError("Should get the balance history of the given account from here.")
    
    
```

#### More Specific Version

A more specific version would look a little like this:

```python
class GenericExecutor(Executor):
    def __init__(self, api:ExternalAPI, creds:ICredentials, validator: IValidation):
        self.api = api
        self.credentials = creds
        self.validation = validator
    
    
    def set_credentials(self, user_creds:UserCreds):
        # Sets the credentials.
        self.credentials.link(user_creds)
    
    def get_api_key(self, user_id:str, exchange:str):
        """ Should return a user credentials object """
        return self.credentials.get_creds_by_user_exchange(user_id, exchange)

    def submit(self, trade:Trade) -> Status:
        # Submit the trade to the trade execution company
        api_creds = self.get_api_key(trade.user_id, trade.exchange)
        status:Status = self.api.submit_order(trade, api_creds)
        return status
    
    def status(self, trade:Trade):
        api_creds = self.get_api_key(trade.user_id, trade.exchange)
        status:Status = self.api.get_status(trade, api_creds)
        return status
        
    
    def cancel(self, trade:Trade):
        api_creds = self.get_api_key(trade.user_id, trade.exchange)
        status:Status = self.api.cancel_order(trade, api_creds)
        return status

    def orders(self, user:UserInfo):
        """ Gets all of the user's orders."""
        api_creds = self.get_api_key(trade.user_id, trade.exchange)
        status:Status = self.api.get_all_orders(trade, api_creds)
        return status

    def openned(self, user:UserInfo):
        api_creds = self.get_api_key(trade.user_id, trade.exchange)
        status:Status = self.api.get_open_orders(trade, api_creds)
        return status
```

Conversely, we would train/backtest using a mock executor, would look like the following:

```python
class MockExecutor(Executor):
    def __init__(self, api:ExternalAPI, creds:ICredentials, validator: IValidation):
        # We'd create mocks for every single one of these parts
        # The mock will let us test the full functionality 
        # A mock API would let us put stochastic logic inside of the API to test for issues with connections and spreads. 
        self.api = api
        self.credentials = creds
        self.validation = validator
    
    
    def set_credentials(self, user_creds:UserCreds):
        # Sets the credentials.
        self.credentials.link(user_creds)
    
    def get_api_key(self, user_id:str, exchange:str):
        """ Should return a user credentials object """
        return self.credentials.get_creds_by_user_exchange(user_id, exchange)

    def submit(self, trade:Trade) -> Status:
        # Submit the trade to the trade execution company
        api_creds = self.get_api_key(trade.user_id, trade.exchange)
        status:Status = self.api.submit_order(trade, api_creds)
        return status
    
    def status(self, trade:Trade):
        api_creds = self.get_api_key(trade.user_id, trade.exchange)
        status:Status = self.api.get_status(trade, api_creds)
        return status
        
    
    def cancel(self, trade:Trade):
        api_creds = self.get_api_key(trade.user_id, trade.exchange)
        status:Status = self.api.cancel_order(trade, api_creds)
        return status

    def orders(self, user:UserInfo):
        """ Gets all of the user's orders."""
        api_creds = self.get_api_key(trade.user_id, trade.exchange)
        status:Status = self.api.get_all_orders(trade, api_creds)
        return status

    def openned(self, user:UserInfo):
        api_creds = self.get_api_key(trade.user_id, trade.exchange)
        status:Status = self.api.get_open_orders(trade, api_creds)
        return status
```



## Test Driven Development

The approach to this should be an interesting process. Here's what I'm seeing so far:


1. The UI should be pretty simple for the executor itself. 
1. If I use dataclasses to guide the parameters I'll be able to reduce the issues.
1. Knowing how to do test driven development on this stuff will be pretty hard (without connecting to a database).
1. It might be possible to test that we have certain outputs well before we get into specifics.
1. It might be possible to check that the broker is getting the right information it needs to make a decision.
    1. Sorting by time appropiately is is a good example.
    1. Another thing to consider is if the query parameters are well received and parsed.
        1. This is especially true because the query system will definitely change in Jamboree v2.
        1. The upcoming change will happen after the training system is complete, though I'll be moving the order system away from the old system to start removing technical debt.
    1. It's possible to create specific DataClass like objects to manage how time is sent to the lower system.
        1. I'd just need to be sure the outputs of that class is proper.