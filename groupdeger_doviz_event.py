#!/usr/bin/env python
# coding: utf-8

# # IMPORT LIBRARIES

# In[1]:


from urllib import request
import xml.etree.ElementTree as ET
import pandas as pd
import sqlite3
from datetime import datetime


# # GET XML FROM URL

# In[2]:


url = 'https://www.tcmb.gov.tr/kurlar/today.xml'
print ("URL:", url)


# In[3]:


html = request.urlopen(url)
data = html.read()
import_time = datetime.now()


# # READ DATA AND WRITE TO DATAFRAME

# In[4]:


df = pd.read_xml(data)
df


# # CREATE SQL TABLE

# In[5]:


connection_obj = sqlite3.connect('test_database')
cursor_obj = connection_obj.cursor()
cursor_obj.execute("DROP TABLE IF EXISTS DovizSQL")
table = """ CREATE TABLE DovizSQL (
            
            CrossOrder VARCHAR(255) NOT NULL,
            Kod VARCHAR(255) NOT NULL,
            CurrencyCode VARCHAR(255) NOT NULL,
            Unit VARCHAR(255) NOT NULL,
            Isim VARCHAR(255) NOT NULL,
            CurrencyName VARCHAR(255) NOT NULL,
            ForexBuying VARCHAR(255) NOT NULL,
            ForexSelling VARCHAR(255) NOT NULL,
            BanknoteBuying VARCHAR(255) NOT NULL,
            BanknoteSelling VARCHAR(255) NOT NULL,
            CrossRateUSD VARCHAR(255) NOT NULL,
            CrossRateOther VARCHAR(255) NOT NULL
        ); """
 
cursor_obj.execute(table)


# In[6]:


#conn = sqlite3.connect('DovizSQL')
c = connection_obj.cursor()

c.execute('CREATE TABLE IF NOT EXISTS DovizSQL (text)')
connection_obj.commit()

df.to_sql('DovizSQL', connection_obj, if_exists='replace', index = False)


# In[7]:


c.execute('''  
SELECT * FROM DovizSQL
          ''')

for x in c.fetchall():
    print(x)
    


# # SUMMARY

# In[8]:


date_alert = "The date of importing the today.xml file is " + str(import_time)


# In[9]:


currency_codes = []
c.execute('''  
SELECT CurrencyCode FROM DovizSQL
          ''')
for data in c.fetchall():
    currency_codes.append(data[0])
    
currency_names = []
c.execute('''  
SELECT CurrencyName FROM DovizSQL
          ''')
for data in c.fetchall():
    currency_names.append(data[0])
    
forex_buying = []
c.execute('''  
SELECT ForexBuying FROM DovizSQL
          ''')
for data in c.fetchall():
    forex_buying.append(data[0])
    
forex_selling = []
c.execute('''  
SELECT ForexSelling FROM DovizSQL
          ''')
for data in c.fetchall():
    forex_selling.append(data[0])


# In[10]:


print("\n" + date_alert)
print("\nCurrencyCode|CurrencyName|ForexBuying|ForexSelling\n")
for i in range(len(currency_codes)):
    print(currency_codes[i] + " | ", end="")
    print(currency_names[i] + " | ", end="")
    print(forex_buying[i], end="")
    print(" | ", end="")
    print(forex_selling[i], end="")
    print(" ")


# In[ ]:




