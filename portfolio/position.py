import json
from portfolio.trade import Trade
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

    def getMktValue(self,price):
        return self.getQuantity() * price
    
    def getQuantity(self):
        return sum([trade.quantity for trade in self.trades])
    
    def getBreakeven(self):
        return self.getMktValue() / self.getQuantity()

    def getPercentPL(self, currPrice):
        return round((currPrice - self.getBreakeven()) / self.getBreakeven() * 100, 2)
    
    def getDollarPL(self, currPrice):
        return round((currPrice - self.getBreakeven()) * self.getQuantity(), 2)

    def getPercentPortfolio(self,totalPortfolioValue):
        return round(self.getMktValue() / totalPortfolioValue * 100, 2)

    def getTradeDataCollums(self,price):
        mktValue = self.getMktValue(price)
        return  {"Type": [trade.trade_type for trade in self.trades],
                "Quantity": [trade.quantity for trade in self.trades],
                "Price": [trade.price for trade in self.trades],
                "$ PL": [trade.dollarPL(price) for trade in self.trades],
                "% PL": [trade.percentPL(price) for trade in self.trades],
                "Mkt Value": [price * trade.quantity for trade in self.trades],
                "% Position": [round(((price * trade.quantity)/mktValue) * 100, 2) for trade in self.trades]
                }

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


    def to_dict(self):
        return {
            "ticker": self.ticker,
            "trades": [trade.to_dict() for trade in self.trades]
        }
    
    def from_dict(data):
        trades = [Trade.from_dict(trade) for trade in data["trades"]]
        return Position(data["symbol"], data["position_type"], data["average_price"], data["quantity"], trades)

    
    def sellPosition(self, st: Trade):
        for lt in self.trades:
            if (lt.trade_type == self.LONG) & (lt.asset == st.asset):
                if (lt.quantity == st.quantity):
                    self.trades.remove(lt)
                    self.p.addCash(st.getValue())
                    return True
        for lt in self.trades:
            if (lt.trade_type == self.LONG) & (lt.asset == st.asset):
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
    



                    


