import os, sys, json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.toolbox import Toolbox as t
from portfolio.portfolio import Portfolio
from portfolio.position import Position
from portfolio.trade import Trade

def newUser(accountValue, loginID):
    p = Portfolio(accountValue)
    t.save_to_json(p, "data/" + loginID + ".json")

newUser(10000, "admin")
