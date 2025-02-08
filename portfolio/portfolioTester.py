
import json
from trade import Trade
from portfolio import Portfolio
from scripts import Toolbox as t

p = Portfolio(10000)

t1 = Trade("APPL", 20.5, 50, "long", "equity")
t2 = Trade("APPL", 23.5, 50, "long", "equity")
#t3 = Trade("APPL", 23, 100, "sell", "equity")
#t3 = Trade("APPL", 23, 50, "sell", "equity")
#t3 = Trade("APPL", 23, 130, "sell", "equity")
t3 = Trade("TSM", 15, 30, "long", "equity")


p.addTrade(t1)
p.addTrade(t2)
p.addTrade(t3)
print(p.cash)
t.print_json(p.to_dict())