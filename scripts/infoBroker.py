import yfinance as yf
import yfinance as yf
import pandas as pd
import json
from toolbox import Toolbox

tb = Toolbox()

t = 'RGTI'
test = yf.Ticker(t)

# Get the most recent price using the history method
#recent_price = test.history(period='1d')
data = test.info
print(json.dumps(data, indent=4))