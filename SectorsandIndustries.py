#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import pandas as pd
from datetime import datetime
from flask import Flask
from sqlalchemy import create_engine
import getpass


# In[2]:


#downloaded total list of all publicly traded stocks in the US from TD Ameritrade
df = pd.read_csv("Sectors.csv")


# In[3]:


df


# In[4]:


app = Flask(__name__)

pw = getpass.getpass()

print("Connected to pgAdmin")
engine = create_engine(f'postgresql://postgres:{pw}@localhost:5432/Final')
con = engine.connect()


# In[5]:


df.to_sql('Sectors',con,if_exists='replace',index=False)


# In[10]:


#df2 = df[['Symbol','Company Name','Market Capitalization','Sector','Industry','Dividend Yield']]
#df2.head()


# In[11]:


#df2["Sector"].unique()


# In[12]:


#df2["Industry"].unique()


# In[13]:


#df3 = df2.groupby(['Sector','Industry'])['Symbol'].count()
#df3


# In[ ]:


if __name__ == '__main__':
    app.run()

