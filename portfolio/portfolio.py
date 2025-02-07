from position import Position
import json
from trade import Trade
from typing import List

class Portfolio():
    def __init__(self, cash: int) {
        self.cash = cash
        self.positons = List[Position]
    }

    def addTrade(self, trade: Trade):
        for p in self.positions:
            if p.ticker == trade.ticker:
                p.addTrade(trade)
                return True
        self.positions.append(Position(self,trade.ticker))
        self.addTrade(trade)
        
    
    def addCash(self,amount):
        self.cash += amount

    def subtractCash(self,amount):
        self.cash -= amount