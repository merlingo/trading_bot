class Rsi_Rule:
    def __init__(self, min,max):
        self.min = min
        self.max = max

    def check(self, data):
        if(data["rsi"]>self.max):
            return "sell"
        elif(data["rsi"]<self.min):
            return "buy"
        else:
            return "keep"