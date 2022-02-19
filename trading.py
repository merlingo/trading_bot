#trend yakalamak icin LSTM egitimi - verileri cek ve vektorleri cikar. verileri trend'e gore etiketle , etiketlenmis verilerle LSTM egit
#LSTM modeli ile asagı/yukari trend var mi karar ver.
#long ac - short ac
#eger long varsa short kararinda onu kapat. eger short varsa long kararinda onu kapat
# zarar var mı hesapla - zarar varsa cikma

class TestVerisiHazirlayici:
    pass
def verileriTagle():
    pass
def split_data(X):
    """
    girilen X verilerini zamana gore test ve train olarak ayirir. Verilerin trend girdilerine gore etiketler
    :param X:
    :return:
    """
    pass
class DataCollector():
    pass
def init(sourcename,sourcetype):
    pass
def anlikDeger(curr,date="now"):
    """
    girilen tarih icin curr olarak girilen varlık vektorunu getirir
    :param date:
    :return: zaman bazli deger vektoru
    """
    pass
def degerler(curr, timespan=[]):
    """
    curr varligi icin tum vektorler
    :param curr:
    :return: zaman bazli degerler matrisi
    """
    pass
def get_features():
    pass
def set_featureFunc(header,func):
    pass
def get_sourcetype():
    pass
def get_sourcename():
    pass

class Trade():
    pass
openTrend=0 #0 yok, -1 short acilmis, +1 long acilmis
giris_degeri=0 #yakalanan trendin baslangic degeri
def open_long():
    pass

def open_short():
    pass

def close_long():
    pass

def close_short():
    pass

def buy():
    if(openTrend>0):
        return 0
    elif(openTrend<0):
        close_short()
    else:
        open_long()
    return 1

def sell():
    if (openTrend < 0):
        return 0
    elif (openTrend > 0):
        close_long()
    else:
        open_short()
    return 1

class DecisionMaker():
    pass
def init(): #set parameter: risk, trend_size,
    pass
def fit():
    pass
def monitor():
    pass
def score(vector):
    pass
def import_model():
    pass
def export_model():
    pass

class Trend():
    """
    yeni bir trend olduguna karar verince trend objesi yaratilir. baslangic degeri, anlik kar zarar hesaplamalari, dusus/artis trend tipi gibi degerler tutulur
    baslat, sonlandir, anlik kar/zarar yazdir, para birimi getir, gibi fonksiyonlari vardir. trend baslatma ve sonlandırma fonksiyonlari trade al sat fonksiyonlarini
    cagirir.
    """
    pass

