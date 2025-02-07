import json
from trade import Trade
from position import Position
from portfolio import Portfolio

p = Portfolio(10000)

t1 = Trade("APPL", "20.5", "100", "long", "equity")
t2 = Trade("APPL", "23.5", "50", "long", "equity")
#t3 = Trade("APPL", "23", "100", "sell", "equity")
#t3 = Trade("APPL", "23", "50", "sell", "equity")
#t3 = Trade("APPL", "23", "130", "sell", "equity")

p.addTrade(t1)
print(p.cash)
print(p.positions)