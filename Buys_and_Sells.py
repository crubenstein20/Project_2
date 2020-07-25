#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import pandas as pd
from datetime import datetime


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


# In[ ]:


def getInsideTrades():
    startTime = datetime.now()
    pages = 4 #After going back 4 pages, the time frame was about 1 week into the past of filings
    finaldf = pd.DataFrame()
    transaction = ['buying','sales']
    webpagesscraped = 0
    for t in transaction:
        for i in range(pages):
            url = f"https://www.insidearbitrage.com/insider-{t}/?desk=yes&pagenum={i+1}" #desktop format
            df = pd.read_html(url)
            df = df[2]
            columns = df.iloc[0]
            df.columns = columns
            df.drop(df.columns[0],axis=1,inplace=True)
            df = df[1:]
            if t == 'buying':
                df['Type'] = "buy"
            else:
                df['Type'] = "sell"
            frames = [finaldf,df]
            finaldf = pd.concat(frames)
            webpagesscraped+=1
            print(f'Scraped Pages:{webpagesscraped}, Running time = {datetime.now() - startTime}')

    finaldf2 = finaldf.rename(columns={"# Shares":"Number of Shares","Value($)":"Value"})
    print(f'Renamed columns: {datetime.now() - startTime}')
    finaldf2.to_csv('BuysandSells.csv')
    print(f'BuysandSells CSV saved: {datetime.now() - startTime}')
    finaldf2.to_sql('BuysandSells',con,if_exists='replace',index=False) #import to postgresql
    print(f'BuysandSells Table Successfully imported to PostgreSQL - Completed in: {datetime.now() - startTime}')


# In[5]:





# In[ ]:


finaldf2


# In[ ]:


if __name__ == '__main__':
    app.run()

