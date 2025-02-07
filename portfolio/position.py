import json
from trade import Trade
from typing import List

class Position:
    LONG = "long"
    SHORT = "short"
    SELL = "sell"
    COVER = "cover"

    def __init__(self, portfolio, ticker: str, trades: List[Trade] = None):
        self.p = portfolio
        self.ticker = ticker
        self.trades = trades if trades else []

    def addTrade(self, trade: Trade):
        if trade.trade_type == "sell":
            if self.sellPosition(trade) == True:
               return True
            else:
               print("ERROR TRADE NOT COMPLETED")
               return False

        elif trade.trade_type == "cover" or trade.trade_type == "short":
            #SHORTING NOT YET IMPLEMENTED  
            pass
        elif trade.trade_type == "long":
            self.trades.append(trade)
            self.p.subtractCash(trade.getValue())


    def toDict(self):
        return {
            "ticker": self.ticker,
            "trades": [trade.to_dict() for trade in self.trades]
        }
    
    def sellPosition(self, st: Trade):
        for i in range(0,len(self.trades)):
            lt = self.trades[i]
            if (lt.trade_type == self.LONG):
                if (lt.quantity == st.quantity):
                    self.trades.remove(i)
                    self.p.addCash(st.getValue())
                    return True
        for i in range(0,len(self.trades)):
            lt = self.trades[i]
            if (lt.trade_type == self.LONG):
                if (lt.quantity > st.quantity):
                    lt.quantity -= st.quantity
                    self.p.addCash(st.getValue())
                    return True
                if (lt.quantity < st.quantity):
                    st.quantity -= lt.quantity
                    self.p.addCash(st.getValue())
                


                    


