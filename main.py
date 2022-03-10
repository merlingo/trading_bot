# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import logging

import ccxt
import time
import pandas as pd
import numpy as np

from stockstats import StockDataFrame as Sdf
from sklearn.ensemble import RandomForestRegressor
from loguru import logger
from Position import *
import datetime

def best_prices(prices):
    prices.sort()
    bsp={}
    bsp["low"] = prices[0]
    bsp["high"]=prices[-1]
    return bsp
def expect(decides,bsp,keep_price=15):
    # -(EKSİ)LER SATIŞ +(ARTI)LAR ALIŞ OLARAK DUSUNULMELİDİR. AŞAĞIDAKİNİN TAM TERSİ
    # 0 -> keep. 1 -> satim at the price 2-> satim at price*1.2 3-> asagi ralli, sat ve bekle ralli bitene kadar bekle
    # -1 -> alim at the price -2 -> alim at price 1*1.2 -3 -> yukari ralli, al ve bekle ralli bitene kadar bekle

    #en iyiler arasi fark 10 dolardan dusukse keep
    if(abs(bsp["high"] - bsp["low"])<keep_price):
        return 0
    #eger decides sayilari cikarilir. aralarindaki fark 9-1=8 ya da 8-2=6 ise ralli, 7-3=4 ise katli, 6-4 ise degerinde, 5-5 ise keep
    bc = decides.count("al")
    sc = decides.count("sat")
    if((sc-bc)>=8): #satış sayısı daha coksa - karar listesinde daha çok satış vardır
        return 3
    elif((sc-bc)<=-8): #buy count alış sayısı daha çoksa
        return -3
    return (sc-bc)/2

def etiketle(df,karar_range=7):
    #veride change - sat + al olmaktadir
    #verinin ileri dogru etiketlenmesi - veri üstüste al sat degerlerine bakilir. üstüste 30 al ya da 10 sat varsa ralli olur. 3-4 al ya da sat arasina bir iki degisim varsa da ralli bozulmaz
    #ralli icindeki tumu ralli olarak etiketlenir.
    Y=[]
    prices=[]
    changes = []
    for index,(i, row) in enumerate(df.iterrows()):
        #verinin geri dogru etiketlenmesi - i+10. siraya gelince, i'deki veri 10 deger icindeki en iyi alma ve satma degeri cikarilir.
        #decide = "al" if row["change"] < 0 else "sat"

        prices.append((row["high"]+row["low"])/2)
        if(len(prices) >1):
            changes.append((prices[index]-prices[index-1])/prices[index])
        #if(index<len(df)-karar_range):

        if(index >=karar_range-1):
            cs = sum(changes[(index - karar_range):index-1])
            if (cs > 0):  # degisim 0dan büyük ozaman alinsin
                if(len(Y)>0 and Y[-1]>0 and cs>Y[-1]):
                    Y.append(+2)
                else:
                    Y.append(+1)
            elif (cs < 0):  # degisim 0dan kucuk ozaman satilsin
                if(len(Y)>0 and Y[-1]<0 and cs<Y[-1]):
                    Y.append(-2)
                else:
                    Y.append(-1)
            else:  # degisim 0. oldugu yerde kalsin
                Y.append(0)
            #buySellPrices = best_prices(prices[(index-karar_range):index])
            # geriye doğru her bir satirdaki deger icin, ileriye dönük 10 degisimin toplamına göre, al ya da sat kararı olusturulmaktadir.
            #eger sonraki 10 degisim degeri 0'dan kucukse demekki fiyat düsmüstür. ozaman o fiyat icin sat emri olusmaktadir.
            #decides = ["sat" if sum([c for c in df[i+1:i+karar_range]["change"]])<0 else "al" for i in range(index-karar_range,index)]
            #Y.append(expect(decides,buySellPrices))

            #print("Y:",Y[index+1-karar_range],"\nchanges:",changes[(index-karar_range)+1:index-1],"\nfiyatlar:",prices[(index-karar_range)+1:index])
    for i in range(len(Y),len(changes),1):
        Y.append(-1 if changes[i]<0 else 1)
    Y.append(0)
    return Y # y, order {alim: deger, satim:deger} ya da keep den olusur.

def rf_train(model=None,n_times=3):
    i=1
    if(model==None):
        rf = RandomForestRegressor()
    else:
        rf=model
    while(i<=n_times):
        stock, exchange = load_data()
        X, Y = prepare_dataset(stock)
        rf.fit(X, Y)
        print("model egitimi tamamlandı: ",i,"/",n_times,"\n 3 dk beklenecek.")
        if(i==n_times):
            break
        sleep(60*2)
        i+=1
    return rf


def load_data():
    try:
        exchange_id = 'binance'
        exchange_class = getattr(ccxt, exchange_id)
        exchange = exchange_class({
            #'apiKey': 'aRkwszijDLpJiBKsPuuJJ7evVFz4OlYWHDTnXl85MQuBPKvAcl6IWCjGVsejXeJK',
            #'secret': 'Dq57pLUvMKnC0oQUVVNn2A14XMap4GiFXempfw0qer06FZCk77EZQKSjj0pBsf7l',
            # nazli
            'apiKey': 'ztvYJKf1lZ58nnWReDYu6XDukelYf1EhbfGw3itMRwQ6NDqCVTg2aFAzfT1tuS8T',
            'secret': 'lfwZnQvbT1HcGfUrajCdFdmYN2FL8i4GjmZl5rekgo9NLIVIJ3yVk2VKOQMD55It',
            'timeout': 30000,
            'enableRateLimit': True,
            'verbose': False
        })
        exchange.set_sandbox_mode(False)
        exch = 'binance'  # initial exchange
        t_frame = '1m'  # 1-day timeframe, usually from 1-minute to 1-week depending on the exchange
        symbol = 'BTC/USDT'  # initial symbol        exchange.load_markets(True)
    except AttributeError:
        print('-' * 36, ' ERROR ', '-' * 35)
        print('Exchange "{}" not found. Please check the exchange is supported.'.format(exch))
        print('-' * 80)
        quit()
    if exchange.has["fetchOHLCV"] != True:
        print('-' * 36, ' ERROR ', '-' * 35)
        print('{} does not support fetching OHLC data. Please use another  exchange'.format(exch))
        print('-' * 80)
        quit()
    if (not hasattr(exchange, 'timeframes')) or (t_frame not in exchange.timeframes):
        print('-' * 36, ' ERROR ', '-' * 35)
        print('The requested timeframe ({}) is not available from {}\n'.format(t_frame, exch))
        print('Available timeframes are:')
        for key in exchange.timeframes.keys():
            print('  - ' + key)
        print('-' * 80)
        quit()
    try:
        # start_date = int(datetime.datetime(2021, 1, 1, 10, 20).timestamp() * 1000)
        data = exchange.fetch_ohlcv(symbol, t_frame, limit=400)
        data = [[exchange.iso8601(candle[0])] + candle[1:] for candle in data]
        header = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'volume']
        df = pd.DataFrame(data, columns=header)
        stock = Sdf.retype(df)
        # stock = stock[["rsi_14","cci_10","atr_13","high_15_sma","macd","ppo"]]
        stock.init_all()
    except Exception as e:
        print('-' * 36, ' ERROR ', '-' * 35)
        print(e)
        print('Exchange "{}" not found. Please check the exchange is supported.'.format(symbol))
        print('-' * 80)
        quit()
    return stock,exchange

def prepare_dataset(stock):
    stock = stock.iloc[5:]#ilk 5 deger hatali hesaplama - karari bozuyor

    Y = etiketle(stock)
    X = stock.iloc[:, ~stock.columns.isin(['timestamp', 'open', 'high', 'low', 'close'])]
    X.fillna(0)
    X.replace({-np.inf: -1_000_000, np.inf: 1_000_000}, inplace=True)
    #print(X.columns)
    #print("len of column:", len(X.columns), " len of rows:", len(X))
    #print("len of Y: ", len(Y))

    # or (index,x),y in zip(stock.iterrows(),Y):
    #    print((x["high"]+x["low"])/2,y)
    # AI egitim
    X = np.nan_to_num(X.to_numpy())
    # print(X)
    X = np.asarray(X).astype(np.float_)
    Y = np.asarray(Y).astype(np.int_)
    return X,Y

def last(exchange,coin,t_frame):
    exchange.load_markets(True)
    data = exchange.fetch_ohlcv(coin, t_frame, limit=25)
    data = [[exchange.iso8601(candle[0])] + candle[1:] for candle in data]
    header = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'volume']
    df = pd.DataFrame(data, columns=header)
    stock = Sdf.retype(df)
    # stock = stock[["rsi_14","cci_10","atr_13","high_15_sma","macd","ppo"]]
    stock.init_all()
    stock.fillna(0)

    stock = stock.iloc[:, ~stock.columns.isin(['timestamp', 'open', 'high', 'low', 'close'])]
    stock.replace({-np.inf: -1_000_000, np.inf: 1_000_000}, inplace=True)
    return stock.iloc[-1]

def decide_ai(model,x):
    d = model.predict([x])
    if(d>0):
        return "buy"
    else:
        return "sell"
def get_price(exchange):
    reloadedMarkets = exchange.load_markets(True)  # force HTTP reload = True
    # print(reloadedMarkets[coin_pair])
    bticker = exchange.fetch_ticker("BTC/USDT")
    # print("ticker: !!!!\n",ticker)
    #print("bid:", float(bticker["bid"]))
    #print("ask:", float(bticker["ask"]))
    bitcoinBTC = (float(bticker["ask"]) + float(bticker["bid"])) / 2
    return bitcoinBTC

def main():
    cont=True
    logger.add("/home/mert/Belgeler/Projeler/app.log", rotation="12:00")  # New file is created each day at noon
    logger.info("Trading bot başlıyor")
    print("ana veri cekiliyor:")
    stock, exchange = load_data()
    X, Y = prepare_dataset(stock)
    logger.info("AI modeli olusturuluyor")
    model = rf_train()
    #filename = '{}.csv'.format("binance_1d")
    spot_asset = "BTC"
    coin_pair = spot_asset + '/USDT'
    limit = 4
    amount = 60  # $ dolar
    #ex = Exchange(spot_asset, exchange, yuzde, limit=limit)
    t=0
    last_d = 0
    plist = PositionList(exchange,limit)
    toplam_kar=0
    old_prices = []
    ever_max_price=-1
    ever_min_price=100000000000000
    ever_prices=[]
    while (cont):
        t+=1
        if(t==60*60):
            logger.info("AI modeli yenileniyor:")
            print("ana veri cekiliyor:")
            stock, exchange = load_data()
            plist.ex = exchange
            #X, Y = prepare_dataset(stock)
            logger.info("AI modeli 1 saatin sonunda tekrar oluşturuluyor.")
            model = rf_train(model,3)
            spot_asset = "BTC"
            coin_pair = spot_asset + '/USDT'
            #ex = Exchange(spot_asset, exchange, yuzde, limit=limit)
            t=0
        try:
            price = round(get_price(exchange), 2)
            if(len(ever_prices)>50):
                ever_prices = ever_prices[1:] #ilkini sil
            ever_prices.append(price)

            if(len(ever_prices)>20):
                if( max(ever_prices)>ever_max_price ):
                    ever_max_price = max(ever_prices)
                    miktar = amount / float(ever_max_price)
                    toplam_kar += plist.evaluate(ever_max_price, miktar, "sell")
                    logger.info("gelmiş geçmiş en büyük değer SATİS emri yakalandi: {} ",ever_max_price)
                    sleep(1)
                elif(min(ever_prices)<ever_min_price ):
                    ever_min_price = min(ever_prices)
                    miktar = amount / float(ever_min_price)
                    toplam_kar += plist.evaluate(ever_min_price, miktar, "buy")
                    logger.info("gelmiş geçmiş en büyük değer  ALİS emri yakalandi: {}",ever_min_price)
                    sleep(1)

            x = last(exchange,coin_pair,t_frame = '1m')
            #decision - sign degisimi tespit edilir. -'ye gectiginde sat, +ya degistiginde al. pozisyon kapatilir.
            d = model.predict([x])
            #logger.info("d:",d," bir onceki karar:",last_d)


            old_prices.append(price)
            avg = sum(ever_prices) / len(ever_prices)
            if (d > 0 and last_d < 0 and price<avg):  # sign degisimi - -dan +ye dondu. cıkacak. al.
                decision = "buy"
                #price =price if len(old_prices)==0 else min(old_prices)
                old_prices = []
            elif (d < 0 and last_d > 0 and price>avg):  # +den -ya döndü. düşecek sat
                decision = "sell"
                #price =price if len(old_prices)==0 else max(old_prices)
                old_prices = []
            else:
                decision = "keep"
            last_d = d
            miktar = amount / float(price)  # kac adet alinacagi - ilgili para biriminin degerini, ortaya koymak istedigimiz dolara boluyoruz
            #logger.info("price:",price,"miktar:",miktar,"decision",decision)

            #ex.order(price, miktar, decision)
            #decision="buy"
            if(len(old_prices)>10):
                if(price == min(old_prices)):
                    decision="buy"
                elif(price==max(old_prices)):
                    decision="sell"
                elif(decision=="keep" and len(plist.list)>0 and plist.list[0].state=="sell"):
                    price = min(old_prices)
                    decision="buy"
                elif(decision=="keep" and len(plist.list)>0 and  plist.list[0].state=="buy"):
                    price = max(old_prices)
                    decision="sell"
                logger.info("Oldprice Birikti!  eski fiyat sayisi {} - KARAR: {} - PRICE:{}", len(old_prices),decision,price)
                old_prices=[]
            #decision="buy"
            plist.evaluate(price,miktar,decision)
            logger.info("toplam kar: {}\n\n", plist.toplam_kar)
            balances = exchange.fetchBalance()["info"]["balances"]
            assets = ["BTC", "USDT"]
            for b in balances:
                if (b["asset"] in assets):
                    logger.info("{}  -  {} (free) : {} (locked)", b["asset"] , b["free"] ,b["locked"])
            if(len(plist.list)>0):
                logger.info("Pozisyon listesi:")
                for p in plist.list:
                    logger.info("price: {} - karar: {} - KapaniyorMu: {}",p.price,p.state, p.kapaniyor)

            time.sleep(1)
            logger.info(".\n")
        except Exception as e:
            logger.info("{}",e)
            continue
        #order
        #stock.to_csv("D:\\Projeler\\Trading\\trading_py\\binance_1d.csv")

if __name__ == "__main__":
    main()