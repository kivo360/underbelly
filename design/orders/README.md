# Order System

The portfolio order management system is notably the complex component of the event driven backtesting system. Its reponsible for:

1. To keep track of the state of all orders for a given user.
1. Communicate with the broker/exchange.
1. Keep track of the history of orders to do analytics on.
1. Have some rules to drop orders if they turn out to linger too long.
1. Provide information for the total value of the portfolio (open positions that can't be used).
1. Keep track of the slippage of orders.
1. Account for errors that happen.