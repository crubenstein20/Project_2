#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import pandas as pd
import pandas_datareader as dr #get stock info from yahoo
from datetime import datetime, date, timedelta
startTime = datetime.now()


# In[2]:


from flask import Flask
from sqlalchemy import create_engine
import getpass


# In[3]:


app = Flask(__name__)

pw = getpass.getpass()

print("Connected to pgAdmin")
engine = create_engine(f'postgresql://postgres:{pw}@localhost:5432/Final')
con = engine.connect()


# In[4]:


df = pd.read_sql('BuysandSells',con,index_col=0)


# In[5]:


tickerInfo = {}
days = 200 #200 moving average is a popular moving average Traders use


# In[6]:


print('Estimated time of run 8-9 mins.')
def getStock(ticker,n):
    try:
        tickerdf = dr.data.get_data_yahoo(ticker,start = date.today() - timedelta(365) , end = date.today())
        currentprice = tickerdf.iloc[-1]['Close']
        MA = pd.Series(tickerdf['Close'].rolling(n, min_periods=0).mean(), name='200_MA')
        currentma = MA[-1]
        return (currentprice,currentma)
        
    except:
        return ('n/a','n/a')
    
def getPrice(row):
    ticker = row['Symbol']
    if ticker not in tickerInfo.keys():
        tickerinfo = getStock(ticker,days)
        tickerInfo[ticker] = {}
        tickerInfo[ticker]["price"] = tickerinfo[0]
        tickerInfo[ticker]["ma"] = tickerinfo[1]
        return tickerInfo[ticker]["price"]
    else:
        return tickerInfo[ticker]["price"]

def getMovingAverage(row):
    ticker = row['Symbol']
    return tickerInfo[ticker]["ma"]

df['Current_Price'] = df.apply (lambda row: getPrice(row), axis=1)
df['200_Moving_Average'] = df.apply (lambda row: getMovingAverage(row), axis=1)

df.to_csv('CurrentPrice.csv')
print(f'CurrentPrice CSV saved. Completed In: {datetime.now() - startTime}')
df.to_sql('CurrentPrice',con,if_exists='replace',index=False)
print(f'CurrentPrice Table Uploaded to pgAdmin. Completed In: {datetime.now() - startTime}')

print(f'Finally!: {datetime.now() - startTime}')


# In[ ]:


df.head()


# In[ ]:


if __name__ == '__main__':
    app.run()

