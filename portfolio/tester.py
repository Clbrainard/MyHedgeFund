from scripts.toolbox import Toolbox as t
from portfolio.portfolio import Portfolio

p = Portfolio(0)
p = t.save_to_json(p, "data/portfolio.json")