class Rsi_Rule:
    def __init__(self, min,max):
        self.min = min
        self.max = max

    def decide(self, data):
        print("Data: ", data)
        print("Min: ", self.min, " - Max: ", self.max)
        if(float(data)>=float(self.max)):
            return "sell"
        elif(float(data)<=float(self.min)):
            return "buy"
        else:
            return "keep"
    def get_min(self):
        return self.min
    def get_max(self):
        return self.max
    def set_min(self,min):
        self.min = min  
    def set_max(self,max):
        self.max = max