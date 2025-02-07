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
        if trade.trade_type == self.SELL:
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
            "trades": [trade.toDict() for trade in self.trades]
        }
    
    def sellPosition(self, st: Trade):
        for lt in self.trades:
            if (lt.trade_type == self.LONG):
                if (lt.quantity == st.quantity):
                    self.trades.remove(lt)
                    self.p.addCash(st.getValue())
                    return True
        for lt in self.trades:
            if (lt.trade_type == self.LONG):
                if (int(lt.quantity) > int(st.quantity)):
                    lt.quantity = int(lt.quantity) - int(st.quantity)
                    self.p.addCash(st.getValue())
                    return True
                if (int(lt.quantity) < int(st.quantity)):
                    st.quantity = int(st.quantity) - int(lt.quantity)
                    self.p.addCash(float(lt.quantity) * float(st.price))
                    self.trades.remove(lt)
                    self.sellPosition(st)
        return False
    



                    


