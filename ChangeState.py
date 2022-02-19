class ExchangeState():
    "EXCHANGE STATE: AMAC DUSUKTEN ALIP YUKSEKTEN SATMAK"
    def __init__(self,ex):
        #print("ExchangeState: Change state is initilazing: EXCHANGE STATE: AMAC DUSUKTEN ALIP YUKSEKTEN SATMAK")
        self.ex = ex

    def orderBuy(self, price,miktar):
        raise NotImplementedError("Subclass must implement this abtract method")
    def orderSell(self, price,miktar):
        raise NotImplementedError("Subclass must implement this abtract method")
    def stateName(self):
        raise NotImplementedError("Subclass must implement this abtract method")


class BuyOrderState(ExchangeState):
    def __init__(self,ex,order,kar):
        ExchangeState.__init__(self,ex)
        self.ex.check=True
        self.ex.trigger()
        self.order = order
        self.kar = kar
        print("BuyOrderState: alis emri acildi: ",order)
    def orderBuy(self, price,miktar):
        #alis emri durumundayken alis emri verildi. Bir aksiyon alinmaz. Belki ilerde updateOrder yapilir.
        print("BuyOrderState:alis emri durumundayken alis emri verildi. Bir aksiyon alinmaz. Belki ilerde updateOrder yapilir.")

    def orderSell(self, price,miktar):
        #alis emri durumundayken satis emri verildi. Alis emri iptal edilir ve satis emri verilir.
        print("BuyOrderState: alis emri durumundayken satis emri verildi. Bir aksiyon alinmaz. Belki ilerde Alis emri iptal edilir ve satis emri verilir.")
        """
       self.ex.cancelOrder(self.order)
        for p in self.ex.buy_prices:
            if (p[0]==self.order):
                self.ex.buy_prices.remove(p)
        if (len(self.ex.buy_prices)==0):
            self.ex.ChangeState(NothingState())
        """

            
    def stateName(self):
        return "BuyOrder"

class SellOrderState(ExchangeState):
    def __init__(self,ex,order,kar):
        ExchangeState.__init__(self,ex)
        self.ex.check=True
        self.ex.trigger()
        self.order = order
        self.kar=kar
        print("SellOrderState: satis emri acildi: ",order)

    def orderBuy(self,price,miktar):
        #satis emri durumundayken alis emri verildi. satis emri iptal edilir ve alis emri verilir.Belki ilerde satis emri iptal edilir ve alis emri verilir.
        print("SellOrderState:",price," ",miktar)
        """
        self.ex.cancelOrder(self.order)
        for p in self.ex.sell_prices:
            if (p[0]==self.order):
                self.ex.sell_prices.remove(p)
        if (len(self.ex.buy_prices)==0):
            self.ex.ChangeState(NothingState())
        """
    def orderSell(self,price,miktar):
        #satis emri durumundayken satis emri verildi. Bir aksiyon alinmaz. Belki ilerde updateOrder yapilir
        print("SellOrderState: ",price," ",miktar)
    def stateName(self):
        return "SellOrder"

class ExistState(ExchangeState):
    def __init__(self,ex):
        ExchangeState.__init__(self,ex)
        self.ex.check=False
        self.ex.exState = "Buy"
    def orderBuy(self,price,miktar):
        #zaten varken alis emri verildi. listedeki en dusuk elamanin onceki fiyatin altina indiyse bir daha al. listede l(default=20) olana kadar devam olunca alma.
        #print("ExistState: ALIS Durumunda BUY emri verildi: price:",price,"   -   price_list:",self.ex.buy_prices)

        if(len(self.ex.buy_prices) <=self.ex.limit):
            #print("ExistState: limit ", self.ex.limit, " doldu. Alis emri verilmez. Aynen devam:\n",self.ex.buy_prices)
            last = self.ex.buy_prices[0] #en dusuk eleman en basta.
            if(price<last[0]-self.ex.range):
                #print("ExistState.buy: zaten varken alis emri verildi. onceki fiyatin( ",last, ") altina indi. Alınıyor: ",price," - ",miktar)
                order = self.ex.createOrder(price,miktar,t="buy")
                self.ex.ChangeState(BuyOrderState(self.ex,order,0))
                self.ex.buy_prices.append((price,miktar))
                self.ex.buy_prices.sort()
                return

        #print("Alış emri verilmedi Kar var mı Bakılıyor:",price," - ",last[0])
        price_list = self.ex.buy_prices
        price_list.reverse()  # en yuksek en basa
        bp = None
        #print("ALIS Durumunda SELL emri: price:", price, "   -  buy price_list:", price_list)
        for b in price_list:  # en yuksekten dusuge dogru bakilir. Eger fiyat en yuksekten dusuge gectigi deger bulunursa ordan satis islemine baslanir.
            if (price > b[0] + self.ex.kar_range):
                bp = b
                break
        # last = self.ex.buy_prices[-1]  # en yuksek eleman en sonda.
        if (bp != None):
            miktar = bp[1]
            order = self.ex.createOrder(price, miktar, t="sell")
            self.ex.buy_prices.remove(bp)
            kar = price * miktar - bp[0] * miktar
            self.ex.ChangeState(SellOrderState(self.ex, order,kar))

            self.ex.toplam_kar += kar
            #print("Kar bulundu. Satış yapılıyor.Emir, Kar ile kapatıldı. Kar:",kar, " - ",self.ex.toplam_kar)
        self.ex.buy_prices.sort()

    def orderSell(self,price,miktar):
        #Varken satis emri verildi. buy_prices(dusukten alinanlar) listesindeki en dusukten bakmaya basla(en yuksekten de olabilir denenecek).
        #kar edilen bir alis fiyati yakalayinca o fiyati ve miktari cek. okadarlik satis yap. o alis i listeden sil. eger liste bosaldiysa durumu nothing getir.
        price_list = self.ex.buy_prices
        price_list.reverse() # en yuksek en basa
        bp = None
        #print("ExistState: ALIS Durumunda SELL emri verildi: price:",price,"   -  buy price_list:",price_list)

        for b in price_list: # en yuksekten dusuge dogru bakilir. Eger fiyat en yuksekten dusuge gectigi deger bulunursa ordan satis islemine baslanir.
            if (price > b[0]+self.ex.kar_range):
                bp = b
                break
        #last = self.ex.buy_prices[-1]  # en yuksek eleman en sonda.
        if (bp != None):
            miktar = bp[1]
            order = self.ex.createOrder(price,miktar,t="sell")
            self.ex.buy_prices.remove(bp)
            kar=price*miktar - bp[0]*miktar
            self.ex.ChangeState(SellOrderState(self.ex,order,kar))

            self.ex.toplam_kar += kar
            #print("ExistState.sell: Varken satis emri verildi. En dusuk alis emrinden yüksek satis geldi. Emir, Kar ile kapatıldı. Kar:",kar, " ",self.ex.toplam_kar)
        self.ex.buy_prices.sort()

    def stateName(self):
        return "BuyExist"

class SellExistState(ExchangeState):
    def __init__(self,ex):
        ExchangeState.__init__(self,ex)
        self.ex.check=False
        self.ex.exState = "Sell"
    def orderBuy(self,price,miktar):
        #zaten satilmisken alis emri verildi.  sell_prices(yüksekten satılanlar) listesine en yüksekten bakmaya basla(en dusuk de olabilir).
        #daha yuksege ciktiysa  o fiyati ve miktarı cek. okadarlik alis yap. o satisi listeden sil. eger liste bosaldiysa durumu nothing getir.
        price_list = self.ex.sell_prices # en dusuk en basta kalsin
        #price_list.reverse()
        price_list.sort() #en dusuk basta
        #print("SellExistState: Satis Durumunda alis emri verildi: price:",price,"   -   sel_price_list:",price_list)
        sp = None

        for b in price_list: # en dusukten yuksege dogru bakilir. Eger fiyat en dusukten dusukse gectigi deger bulunursa ordan alis islemine baslanir.
            if (price < b[0]-self.ex.kar_range):
                sp = b
                break
        #last = self.ex.buy_prices[-1]  # en yuksek eleman en sonda.
        if (sp != None):
            miktar = sp[1]
            order = self.ex.createOrder(price,miktar,t="buy")
            if (order == -1):
                return
            self.ex.sell_prices.remove(sp)
            kar= sp[0]*miktar - price*miktar
            self.ex.ChangeState(BuyOrderState(self.ex,order,kar))

            self.ex.toplam_kar += kar

            #print("SellExistState.buy: satis varken alis emri verildi. En yuksek satis emrinden yuksek alis geldi. Emir, Kar ile kapatıldı. Kar:",kar," ",self.ex.toplam_kar )

    def orderSell(self,price,miktar):
        #satis varken satis verildi. en yuksek satis fiyatindan daha yuksege ciktiysa satis yap ve listeye ekle.
        #listede en fazla l (default:20) olana kadar ekle.

        #print("SATIS Durumunda SELL emri: price:",price,"   -   price_list:",self.ex.sell_prices)
        self.ex.sell_prices.sort()
        last = self.ex.sell_prices[-1] #en yuksek eleman en sonda.
        if(len(self.ex.sell_prices) <=self.ex.limit):
            #print("limit ", self.ex.limit, " doldu. Satis emri verilmez. Aynen devam:\n",self.ex.sell_prices)
            if(price>last[0]+self.ex.range):
                #print("SellExistState.sell: satis emri verildi. onceki fiyatin( ",last, ") ustune cikti. Satiliyor: ",price, " - ",miktar)
                order = self.ex.createOrder(price,miktar,t="sell")
                if (order == -1):
                    return
                self.ex.sell_prices.append((price,miktar))
                self.ex.ChangeState(SellOrderState(self.ex,order,0))
                self.ex.sell_prices.sort()
                return

        #print("Satis emri verilmedi kar var mı bakiliyor:",price," - ",last[0])
        sp = None
        for b in self.ex.sell_prices:  # en dusukten yuksege dogru bakilir. Eger fiyat en dusukten dusukse gectigi deger bulunursa ordan alis islemine baslanir.
            if (price < b[0] - self.ex.kar_range):
                sp = b
                print("kar bulundu: Alış emri veriliyor.")
                break
        if (sp != None):
            miktar = sp[1]
            order = self.ex.createOrder(price, miktar, t="buy")
            if (order == -1):
                return
            self.ex.sell_prices.remove(sp)
            kar = sp[0] * miktar - price * miktar
            self.ex.ChangeState(BuyOrderState(self.ex, order,kar))

            self.ex.toplam_kar += kar
            self.ex.sell_prices.sort()

    def stateName(self):
        return "SellExist"

class NothingState(ExchangeState):
    def __init__(self,ex):
        ExchangeState.__init__(self,ex)
        self.ex.check=False
    def orderBuy(self,price,miktar):
        #Yokken alis emri verildi. Alis emri verilir. alis listesine eklenir.
        #print("NothingState.buy: Yokken alis emri verildi. Alis emri verilir.")

        order = self.ex.createOrder(price,miktar,t="buy")
        if(order==-1):
            return
        self.ex.buy_prices.append((price,miktar))
        self.ex.ChangeState(BuyOrderState(self.ex,order,0))
    def orderSell(self,price,miktar):
        #Yokken satis emri verildi. satis emri verilir. satis listesine eklenir.
        #print("NothingState.sell: Yokken satis emri verildi. satis emri verilir.")

        order =self.ex.createOrder(price,miktar,t="sell")
        if(order==-1):
            return
        self.ex.sell_prices.append((price,miktar))
        self.ex.ChangeState(SellOrderState(self.ex,order,0))
    def stateName(self):
        return "Nothing"