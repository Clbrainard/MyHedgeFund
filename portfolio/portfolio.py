from position import Position
import json
from trade import Trade
from typing import List

class Portfolio():

    def __init__(self, cash: int):
        self.cash = cash
        self.positions = []

    def addTrade(self, trade: Trade):
        for p in self.positions:
            if p.ticker == trade.ticker:
                p.addTrade(trade)
                return True
        new_position = Position(self, trade.ticker)
        if (new_position.addTrade(trade)):
           return False
        self.positions.append(new_position)
    
    def addCash(self,amount):
        self.cash += amount

    def subtractCash(self,amount):
        self.cash -= amount

    def toDict(self):
        return {
            'cash': self.cash,
            'positions': [p.toDict() for p in self.positions]
        }