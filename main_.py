import ccxt
import os 
import re
import time
import pandas as pd
from Exchange import Exchange
from stockstats import StockDataFrame as Sdf
def get_historical_data(coin_pair, timeframe,exchange):
    """Get Historical data (ohlcv) from a coin_pair
    """
    # optional: exchange.fetch_ohlcv(coin_pair, '1h', since)
    data = exchange.fetch_ohlcv(coin_pair, timeframe)
    # update timestamp to human readable timestamp
    data = [[exchange.iso8601(candle[0])] + candle[1:] for candle in data]
    header = ['Timestamp', 'Open', 'High', 'Low', 'Close','volume']
    df = pd.DataFrame(data, columns=header)
    return df

def get_rsi():
    pass

def get_price(exchange):
    reloadedMarkets = exchange.load_markets(True)  # force HTTP reload = True
    # print(reloadedMarkets[coin_pair])
    bticker = exchange.fetch_ticker("BTC/USDT")
    # print("ticker: !!!!\n",ticker)
    #print("bid:", float(bticker["bid"]))
    #print("ask:", float(bticker["ask"]))
    bitcoinBTC = (float(bticker["ask"]) + float(bticker["bid"])) / 2
    return bitcoinBTC

def create_stock(historical_data):
    """Create StockData from historical data 
    """
    stock  = Sdf.retype(historical_data)
    return stock
def decide_rsi(ind_vec):

    if(ind_vec["rsi"]>60 ):
        price = ind_vec["price"] #if (ind_vec["rsi"]>40 and ind_vec["rsi"]<50)  else ind_vec["price"]+10
        return "sell",price
    elif(ind_vec["rsi"]<40   ):
        price = ind_vec["price"] #if (ind_vec["rsi"]>38 and ind_vec["rsi"]<50) else ind_vec["price"]-10
        return "buy",price
    else:
        return "keep",ind_vec["price"]
    
def main():
    #read config file
    cont = True
    exchange_id = 'binance'
    exchange_class = getattr(ccxt, exchange_id)
    exchange = exchange_class({
        #test
        #'apiKey': 'aRkwszijDLpJiBKsPuuJJ7evVFz4OlYWHDTnXl85MQuBPKvAcl6IWCjGVsejXeJK',
        #'secret': 'Dq57pLUvMKnC0oQUVVNn2A14XMap4GiFXempfw0qer06FZCk77EZQKSjj0pBsf7l',
        #mert
        #'apiKey': '69VQHuUL2rmrekKkp3o3SXdLKrkUXkTGt5agEWTj3d33GBkIYHM8AKmQKyl8S1d0',
        #'secret': 'Frol2UbwvQxN62iawMA6sc5IYrzEZxudtIBNg6zyDoXdjbq4nfUSUdwSjSOjpCpf',
        #nazli
        'apiKey': 'ztvYJKf1lZ58nnWReDYu6XDukelYf1EhbfGw3itMRwQ6NDqCVTg2aFAzfT1tuS8T',
        'secret': 'lfwZnQvbT1HcGfUrajCdFdmYN2FL8i4GjmZl5rekgo9NLIVIJ3yVk2VKOQMD55It',
        'timeout': 30000,
        'enableRateLimit': True,
        'verbose': False,
    })

    #exchange.set_sandbox_mode(True)
    spot_asset = "BTC"
    exchange.load_markets(True)

    coin_pair = spot_asset+'/USDT'
    yuzde = 0.5
    limit = 3
    ex = Exchange(spot_asset,exchange,yuzde,limit=limit)

    while(cont):
        #piyasa bilgilerini cek

        """
        exchange.load_markets()  # request markets
        print("market keys:\n",list(exchange.markets.keys()))  # output a short list of market symbols
        reloadedMarkets = exchange.load_markets(True)  # force HTTP reload = True
        #print(reloadedMarkets[coin_pair])
        bticker = exchange.fetch_ticker("BTC/USDT")
        #print("ticker: !!!!\n",ticker)
        print("bid:",float(bticker["bid"]))
        print("ask:",float(bticker["ask"]))
        bitcoinBTC = (float(bticker["ask"])+float(bticker["bid"]))/2
        print("last price BTC:", bitcoinBTC)
        ticker = exchange.fetch_ticker(coin_pair)
        coin_price=((float(ticker["ask"])+float(ticker["bid"]))/2) * bitcoinBTC
        print("last price:", coin_price)
        """
        try:
            data = get_historical_data(coin_pair, '1m',exchange)

            stock_data = create_stock(data)
            # rsi degerini oku
            # stock_data['rsi_14']
            # print("stock_data low price",stock_data['low'].iloc[-1])

            # Get most recent RSI value of our data frame
            # In our case this represents the RSI of the last 1h
            last_rsi = stock_data['rsi_14'].iloc[-1]
            last_vol = stock_data['volume'].iloc[-1]
            last_ma = stock_data['macd'].iloc[-1]
            change = stock_data['change'].iloc[-1]
            price = round(get_price(exchange),2)
            indicator_vec = {"rsi":last_rsi, "vol":last_vol,"macd":last_ma,"price":price,"change":change}
            # amount = ex.amount()  # ortaya koyulacak para - dolar cinsinden
            amount = 80  # $ dolar
            miktar = round(amount / float(price),4)  # kac adet alinacagi - ilgili para biriminin degerini, ortaya koymak istedigimiz dolara boluyoruz
            # print("price - miktar - harcanan:  ",price," - ",miktar," - ",amount)


            # print(decision)
            print("rsi:", last_rsi, " price:", price," last_vol:", last_vol," last_ma:", last_ma)
            # rsi degerine gore karar ver
            decision,price = decide_rsi(indicator_vec)
            # decision="buy"
            # miktar=0.001
            #if(ex.state.stateName() !="Nothing"):
            #    decision = "sell" if len(ex.buy_prices)>0 else "buy"
            print(decision," at ",price)

            ex.order(price, miktar, decision)
            print("toplam kar:", ex.toplam_kar)
            balances = exchange.fetchBalance()["info"]["balances"]
        except:
            continue

        assets = ["BTC", "USDT"]
        for b in balances:
            if(b["asset"] in assets):
                print(b["asset"] +" : "+ b["free"]+"(free)   -   "+b["locked"]+"(locked)\n")
        print("buy prices:",ex.buy_prices)
        print("sell prices:",ex.sell_prices)
        time.sleep (1)
        print(".\n")
        #time.sleep(1)
        #print(".\n")
        #time.sleep (1)
        #print(".\n")
if __name__ == "__main__":
    main()