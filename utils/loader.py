import ccxt
import pandas as pd
from stockstats import StockDataFrame as Sdf
import numpy as np

class Market:
    """
    A class to represent a market and interact with a cryptocurrency exchange.
    Attributes
    ----------
    exchange_id : str
        The ID of the exchange.
    api_key : str
        The API key for the exchange.
    secret : str
        The secret key for the exchange.
    symbol : str
        The trading symbol (e.g., 'BTC/USD').
    exchange : object
        The exchange object created using ccxt.
    t_frame : str
        The timeframe for fetching OHLCV data.
    Methods
    -------
    load_data():
        Initializes the exchange and checks for necessary capabilities.
    get_stock_data(values):
        Fetches OHLCV data from the exchange and returns it as a DataFrame.
    last(values):
        Get the latest OHLCV data from the exchange.
    get_price():
        Fetches the current price of the specified symbol from the exchange.
    """
    def __init__(self, exchange_id, api_key, secret, symbol):
        self.exchange_id = exchange_id
        self.api_key = api_key
        self.secret = secret
        self.symbol = symbol
        self.load_data()

    def load_data(self):
        try:
            exchange_class = getattr(ccxt, self.exchange_id)
            self.exchange = exchange_class({
                'apiKey': self.api_key,
                'secret': self.secret,
                'timeout': 30000,
                'enableRateLimit': True,
                'verbose': False
            })
            self.exchange.set_sandbox_mode(False)
            exch = self.exchange_id  # initial exchange
            self.t_frame = '1m'  # 1-day timeframe, usually from 1-minute to 1-week depending on the exchange
        except AttributeError:
            print('-' * 36, ' ERROR ', '-' * 35)
            print('Exchange "{}" not found. Please check the exchange is supported.'.format(exch))
            print('-' * 80)
            quit()
        if self.exchange.has["fetchOHLCV"] != True:
            print('-' * 36, ' ERROR ', '-' * 35)
            print('{} does not support fetching OHLC data. Please use another  exchange'.format(exch))
            print('-' * 80)
            quit()
        if (not hasattr(self.exchange, 'timeframes')) or (self.t_frame not in self.exchange.timeframes):
            print('-' * 36, ' ERROR ', '-' * 35)
            print('The requested timeframe ({}) is not available from {}\n'.format(self.t_frame, exch))
            print('Available timeframes are:')
            for key in self.exchange.timeframes.keys():
                print('  - ' + key)
            print('-' * 80)
            quit()
    
    def get_stock_data(self, values, limit=400):
        """
        Fetches OHLCV data from the exchange and returns it as a DataFrame.
        Parameters: values (list) - The values to be fetched from the exchange.
                    limit (int) - The number of data points to fetch.
        Returns: stock (DataFrame) - The OHLCV data from the exchange.
        """
        try:
            # start_date = int(datetime.datetime(2021, 1, 1, 10, 20).timestamp() * 1000)
            data = self.exchange.fetch_ohlcv(self.symbol, self.t_frame, limit=limit)
            data = [[self.exchange.iso8601(candle[0])] + candle[1:] for candle in data]

            df = pd.DataFrame(data, columns=values)
            stock = Sdf.retype(df)
            # stock = stock[["rsi_14","cci_10","atr_13","high_15_sma","macd","ppo"]]
            stock.init_all()
        except Exception as e:
            print('-' * 36, ' ERROR ', '-' * 35)
            print(e)
            print('Exchange "{}" not found. Please check the exchange is supported.'.format(self.symbol))
            print('-' * 80)
            quit()
        return stock

    def last(self, values):
        """
        Get the latest OHLCV data from the exchange.
        Parameters: values (list) - The values to be fetched from the exchange.
        Returns: data (DataFrame) - The latest OHLCV data from the exchange.
        """
        self.exchange.load_markets(True)
        #values = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        data =  self.get_stock_data(values, limit=25)# exchange.fetch_ohlcv(coin, t_frame, limit=25)
        data.fillna(0)
        data = data.iloc[:, ~data.columns.isin(values)]
        data.replace({-np.inf: -1_000_000, np.inf: 1_000_000}, inplace=True)
        return data.iloc[-1]
    
    def get_price(self):
        """
         Fetches the current price of the specified symbol from the exchange.
        This method forces an HTTP reload of the market data to ensure the latest
        information is retrieved. It calculates the price as the average of the 
        ask and bid prices.
        Returns:
            float: The average price of the specified symbol.
        """
        self.exchange.load_markets(True)  # force HTTP reload = True
        bticker = self.exchange.fetch_ticker(self.symbol)
        bitcoinBTC = (float(bticker["ask"]) + float(bticker["bid"])) / 2
        return bitcoinBTC