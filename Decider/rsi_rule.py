class Rsi_Rule:
    def __init__(self, min,max):
        self.min = min
        self.max = max

    def decide(self, data):
        print("RSI Rule - Data: ", data)
        print("RSI Rule - Min: ", self.min, " - Max: ", self.max)
        decision=""
        if(float(data)>=float(self.max)):
            decision= "sell"
        elif(float(data)<=float(self.min)):
            decision= "buy"
        else:
            decision= "keep"
        print("RSI Rule - Decision: ", decision)
        return decision
    def get_min(self):
        return self.min
    def get_max(self):
        return self.max
    def set_min(self,min):
        self.min = min  
    def set_max(self,max):
        self.max = max