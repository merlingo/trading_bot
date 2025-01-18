class Rsi_Rule:
    def __init__(self, min,max):
        self.min = min
        self.max = max

    def check(self, data):
        if(data>=self.max):
            return "sell"
        elif(data<=self.min):
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