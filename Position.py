#from ChangeState import *
from loguru import logger
from threading import Thread
from time import sleep

#durum degisimlerinde pozisyon acilir. eger - ise satilir + ise alinir.
def checkOrderThread(id,position,ex, pos_list):
    t=0
    devam=True
    while(devam):
        sleep(3)
        try:
            orders = checkOrderIsOpen(ex)
            ovar=False
            t=0
            for o in orders:
                if (o["id"] ==id):
                    logger.info("devam eden order:",position.price,position.state)
                    if(t==60*5):
                        #order'in suresi doldu. order'ın Pozisyon acmasi ya da kapamasi geri alinir
                        pos_list.orderIptal(id)
                    ovar=True
            if(not ovar):
                logger.info("order tamamlandı:",position.price,position.state)
                #order tamamlandi. pozisyon işlemi tamamlanabilir.
                pos_list.tam_kapat(position)
                devam=False
        except Exception as e:
            logger.info("check order thread exception:",e)
            continue


def order(ex,t,miktar,price,position,pos_list):
    order = ex.create_order('BTC/USDT', 'limit', t, str(miktar), str(price), {'type':'market'})
    thread = Thread(target=checkOrderThread, args=[order["id"],position,ex,pos_list])
    thread.start()
    return order["id"]
def checkOrderIsOpen(ex):
    orders = ex.fetchOpenOrders('BTC/USDT')
    return orders

class Position:
    def __init__(self,ex):
        self.state = "baslangic"
        self.price = 0
        self.miktar=0
        self.id=""
        self.ex =ex
        self.kapaniyor = False
        self.kapa_count=0 # belirli sayida keep'de kapama sayisi artar. Eger bir seviyenin ustune cikarsa keep olmasina bakilmadan kar var mi aranir.
        self.kar =0

    def __str__(self):
        return "id:"+str(self.id)+", "+self.state+", "+str(self.price)+", Kapaniyor:"+str(self.kapaniyor)+"\n"

    def ac(self,price,miktar,karar,pos_list):
        #alis ya da satis pozisyonu acilir.
        self.price = price
        self.miktar = miktar
        self.state = karar

        self.id = order(self.ex, karar, miktar, price,self, pos_list)
        logger.info("pozisyon aciliyor:", self.id, self.price, self.kapa_count,self.state)

    def kapa(self,price,pos_list,karar):
        #alis ise fiyat ustu degerden satis yaparak pozisyon kapatilir.
        #kar =0

        if(karar=="keep" and self.kapa_count<60):
            self.kapa_count+=1
            return False,self.kar
        if(self.state =="buy" and self.price<price ):
            self.kar = self.karHesapla(price)
            order(self.ex,"sell",self.miktar,price,self,pos_list)
            logger.info("pozisyon kapatiliyor:",self.id,self.price,self.state,self.kar )
            self.kapaniyor = True
            return True,self.kar
        elif(self.state=="sell" and self.price>price):
            self.kar  = self.karHesapla(price)
            order(self.ex,"buy",self.miktar,price,self,pos_list)
            logger.info("pozisyon kapatiliyor:",self.id,self.price,self.state,self.kar )
            self.kapaniyor = True
            return True,self.kar
        else:
            return False,self.kar
    def karHesapla(self,price):
        kar = price*self.miktar - self.price*self.miktar
        if self.state=="sell":
            kar = (-1) * kar
        return kar
class PositionList:
    def __init__(self,ex,limit):
        self.list = []
        self.ex=ex
        self.limit = limit
        self.toplam_kar = 0
    def pozisyonAc(self,price,miktar,karar):
        if(karar=="keep"):
            return
        logger.info("Pozisyon aciliyor:",karar," - ",price," - ",miktar)
        p = Position(self.ex)
        p.ac(price,miktar,karar,self)
        #self.list.append(p)
    def pozisyonKapat(self,price,karar):
        kapandi = False
        k=0
        for p in self.list:
            if not(p.kapaniyor):
                d,k = p.kapa(price,self,karar)
                if(d):
                    kapandi = True
                    #logging.warning(msg="Pozisyon kapatılıyor:" + str(p)+"  ----   kar:"+str(k))
                    #break - break ediyoruz çünkü sadece 1 tanesini kapatsın. Ama eger kapaniyorsa hepsini kapatabilir. O fiyatla kapatabilecegi tum pozisyonlari kapatsın gitsin.

        return kapandi,k
    def evaluate(self,price,miktar,karar):

        kap,kar = self.pozisyonKapat(price,karar)
        if(karar=="keep"):
            logger.info("Karar 'keep': islem yapilmadi")
            return 0
        if (kap):
            return kar
        else:
            if(len(self.list)<=self.limit):
                self.pozisyonAc(price,miktar,karar)
            return 0

    def tam_kapat(self,position):
        logger.info("tamamlanan pozisyon:     "+str(position))
        if(position.kapaniyor==True):
            self.toplam_kar += position.kar
            self.list.remove(position)
            logger.info("pozisyon tamamlandı. listeden cikariliyor  - list:"+ str(self.list))
        else:
            logger.info("pozisyon acma tamamlandi - list:"+str(self.list))
            self.list.append(position)

    def orderIptal(self,orderid):
        logger.info("order cancelled:"+str(orderid))
        self.ex.cancelOrder(orderid, 'BTC/USDT')