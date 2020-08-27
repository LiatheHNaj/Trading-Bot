This is a python program that gets price data of coins, (something similar would work with stocks too), computes a technical indicator (moving average) and plots it. 

Developed a strategy that allows us to automatically buy the coin whenever the difference between the price and the moving average is more than 3%. This strategy is also back-tested, IE tested to see if it was profitable in the past.
Using the Binance API. Using the pyti library we'll calculate two moving averages for and using plotly we'll display the data in a nice candlestick plot.

