#!/usr/bin/python

import sys
from datetime import datetime, timedelta

import pandas as pd
import pandas_datareader.data as web

import plotly.plotly as py
import plotly.figure_factory as FF
from plotly.graph_objs import *

if len(sys.argv) > 2:
    print('argument error')
    sys.exit(2)

ticker = sys.argv[1].upper()

try:
    df = web.DataReader(ticker, 'yahoo',
                        datetime(2015, 8, 1), datetime(2017, 4, 1))
except:
    print ticker, 'Not a valid ticker'
    sys.exit(2)

vals = []
for d in df['Close']:
    vals.append(d)

# s is for series
s50_index = df['Close'].keys()
s200_index = df['Close'].keys()

s50_entry = [{'action': stuff} for stuff in pd.Series(vals).rolling(50).mean()]
s200_entry = [{'action': stuff} for stuff in pd.Series(vals).rolling(200).mean()]

dfs50 = pd.DataFrame(s50_entry, index=s50_index)
dfs200 = pd.DataFrame(s200_entry, index=s200_index)

add50_line = Scatter(
    x=dfs50.index,
    y=dfs50.action,
    name='50 day avg',
    line=Line(color='black')
)

add200_line = Scatter(
    x=dfs200.index,
    y=dfs200.action,
    name='200 day avg',
    line=Line(color='blue')
)

# Draws the candlestick
fig = FF.create_candlestick(df.Open, df.High, df.Low, df.Close, dates=df.index)
fig['layout'] .update({
    'title': '50 vs 200 day mean',
    'yaxis': {'title': ticker}
})

# Draws the line averages
fig['data'].extend([add50_line])
fig['data'].extend([add200_line])

py.plot(fig, validate=False, title=ticker)
