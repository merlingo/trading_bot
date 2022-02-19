from ccxt import InvalidOrder, OrderNotFound

from ChangeState import *
from threading import Thread
from time import sleep


def checkOrderIsOpen(ex, spot_asset):
    orders = ex.fetchOpenOrders(spot_asset + '/USDT')
    return orders

def checkOrderThread(self):
    t=0
    while(self.check):
        sleep(1)
        t+=1
        try:
            orders = checkOrderIsOpen(self.ex, self.spot_asset)
            print("toplam kar: ", self.toplam_kar)
            if not((len(orders) > 0)):

                if (len(self.buy_prices) > 0):
                    print("order tamamlandi. Alis prices: ", self.buy_prices)
                    self.ChangeState(ExistState(self))
                elif (len(self.sell_prices) > 0):
                    print("order tamamlandi. Satis prices: ", self.sell_prices)
                    self.ChangeState(SellExistState(self))
                else:
                    self.ChangeState(NothingState(self))
                t=0
                break
            else:
                if(t>=60):
                    print("open orders are time out:",orders)
                    for order in orders:
                        try:
                            self.cancelOrder(order["id"])
                            price = round(order["price"],4)
                            miktar = round(order["amount"],4)
                            if (order["side"] == "buy"):
                                if (self.exState == "Buy"):
                                    self.buy_prices.remove((price, miktar))
                                else:
                                    self.sell_prices.append((price, miktar))
                            else:
                                if (self.exState == "Buy"):
                                    self.buy_prices.append((price, miktar))
                                else:
                                    self.sell_prices.remove((price, miktar))
                            self.toplam_kar -= self.state.kar
                            print(" kar geri alindi:", self.toplam_kar)
                        except Exception as e:
                            t=0
                            print(e)
                            continue
                    t=0
                    break
        except Exception as e:
            print(e)
            continue
class Exchange():
    #pozisyon listesi olacak. degisimlerde pozisyon kapanacak. eger kapanmazsa yeni pozisyon acilacak.
    #
    check = False
    def __init__(self,birim,ex,yuzde,params = {'type':'market'} ,limit=20,range=750,kar_range=7):
        self.spot_asset = birim
        self.state = NothingState(self)
        self.ex = ex
        self.yuzde = yuzde
        self.params = params
        self.sell_prices=[]
        self.buy_prices=[]
        self.limit = limit
        self.range=range
        self.toplam_kar = 0
        self.kar_range = kar_range
        self.exState=""
    def ChangeState(self,state):
        self.state=state
    def checkOrderThread(self,ordertype):
        while(self.check):
            sleep(1000)

            if not(self.checkOrderIsOpen(ordertype)):
                if (len(self.buy_prices)>0):
                    print("order tamamlandi. Alis prices: ", self.buy_prices)

                    self.ChangeState(ExistState(self))
                elif(len(self.sell_prices)>0):
                    print("order tamamlandi. Satis prices: ", self.sell_prices)

                    self.ChangeState(SellExistState(self))
                else:
                    self.ChangeState(NothingState(self))
                """
                if(ordertype=="buy"):
                    self.ChangeState(ExistState())
                else:
                    self.ChangeState(SellExistState())
                """
                break

    def trigger(self):
        thread = Thread(target = checkOrderThread, args = [self])
        thread.start()

    def order(self,price,miktar,t="buy"):
        
        if(t=="buy"):
            self.state.orderBuy(price,miktar)

        elif(t=="sell"):
            self.state.orderSell(price,miktar)

        elif(t=="keep"):
            print("keeping same. Do nothing!!")
        else:
            raise KeyError("Exchance.order HATA: order'in t degeri 'buy' ya da 'sell' olmalidir!!")

    def amount(self):
        #balance degerini ve yuzdeligini al
        result = filter(lambda b: b["asset"]=="USDT", self.ex.fetchBalance()["info"]["balances"])
        price=float(list(result)[0]["free"])*self.yuzde
        print(str(price))
        return price
    def setState(self,state):
        self.state = state
    
    def printState(self):
        print(self.state.stateName)
    
    def listOpenOrders(self):
        orders = self.ex.fetchOpenOrders(self.spot_asset+'/USDT')
        return orders

    def cancelOrder(self,orderid):
        print("order cancelled:"+str(orderid))
        self.ex.cancelOrder(orderid, self.spot_asset+'/USDT')
    
    def createOrder(self,price,miktar,t):
        print("creating new order",price)
        #hangi fiyattan kac adet siparis verilecek
        order=-1
        try:
            order = self.ex.create_order(self.spot_asset+'/USDT','limit',t, str(miktar), str(price), self.params)
        except Exception as e:
            print(e)
            return -1
        finally:
            return order

    def checkOrderIsOpen(self):
        orders = self.ex.fetchOpenOrders(self.spot_asset+'/USDT')
        return ( len(orders)>0)

    def checkMoney(self,ordertype):
        balance = self.ex.fetchBalance()
        asset = self.spot_asset if ordertype=="sell" else "USDT"
        for b in balance:
            if (b["asset"]==asset):
                return b["free"]>0
