

class Trade():
    def __init__(self, 
                 ticker: str, 
                 price: float, 
                 quantity: int, 
                 trade_type: str, #long, sell, short, cover
                 asset: str, #Stock, Call, Put
                 strike: float = None, #for options only
                 expiry: str = None): #for options only
        self.ticker = ticker
        self.price = price
        self.quantity = quantity
        self.trade_type = trade_type
        self.asset = asset
        self.strike = strike if strike else None
        self.expiry = expiry if expiry else None
        

    def to_dict(self):
        return {
            "ticker": self.ticker,
            "price": self.price,
            "quantity": self.quantity,
            "trade_type": self.trade_type,
            "asset": self.asset,
            "strike": self.strike,
            "expiry": self.expiry
        }
    
    def from_dict(data):
        return Trade(**data)
    
    def getValue(self):
        return float(self.quantity) * float(self.price)
    



