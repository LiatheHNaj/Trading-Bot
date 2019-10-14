import pandas as pd
import requests
import json

from pyti.smoothed_moving_average import smoothed_moving_average as sma

from plotly.offline import plot
import plotly.graph_objs as go

class TradingModel:

    def __init__(self, symbol):
        self.symbol = symbol
        self.df = self.getData()

    def getData(self):
        #defining the URL
        base = 'https://api.binance.com'
        endpoint = '/api/v1/klines'
        params = '?&symbol='+self.symbol+'&interval=1h'

        url = base + endpoint + params

        #downloading the data
        data = requests.get(url)
        dictionary = json.loads(data.text)

        #inserting it into dataframe and cleaning it up
        df = pd.DataFrame.from_dict(dictionary)
        df = df.drop(range(6, 12), axis=1)


        #Renaming the columns
        col_names = ['time', 'open', 'high', 'low', 'close', 'volume']
        df.columns = col_names

        for col in col_names:
            df[col] = df[col].astype(float)      #converting the numbers from strings to floats

        # moving average
        df['fast_sma'] = sma(df['close'].tolist(), 10)
        df['slow_sma'] = sma(df['close'].tolist(), 30)

        return df
    # plotting the candlestick chart
    def plotData(self):
        df = self.df

        candle = go.Candlestick(
            x = df['time'],
            open = df['open'],
            close = df['close'],
            high = df['low'],
            low = df['low'],
            name = "Candlesticks");
        #plot MAs
        fsma = go.Scatter(
            x = df['time'],
            y = df['fast_sma'],
            name = "Fast SMA",
            line = dict(color = ('rgba(102, 207, 255, 50)')))
        ssma = go.Scatter(
            x = df['time'],
            y = df['slow_sma'],
            name = "Slow SMA",
            line = dict(color = ('rgba(255, 207, 102, 50)')))

        data = [candle, ssma, fsma]

        #display
        layout = go.Layout(title = self.symbol)
        fig = go.Figure(data = data, layout = layout)

        plot(fig, filename=self.symbol)

def Main():
    symbol = "BTCUSDT"
    model = TradingModel (symbol)
    model.plotData()

if __name__ == '__main__':
        Main()
