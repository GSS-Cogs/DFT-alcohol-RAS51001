#!/usr/bin/env python
# coding: utf-8

# Estimated number of reported drink drive accidents and casualties in Great Britain: 1979 - 2016

# In[1]:


from gssutils import *

scraper = Scraper('https://www.gov.uk/government/statistical-data-sets/ras51-reported-drinking-and-driving')
scraper


# In[2]:


try:
    df = scraper.distribution(
        title='Reported drink drive accidents and casualties in Great Britain since 1979'

    ).as_pandas(sheet_name='RAS51001', start_row = 6,
            row_limit = 39, start_column = 0, column_limit = 12)
    df
except Exception as e:
         print(e.message, e.args)


# In[3]:


table = pd.DataFrame()


# In[4]:


observations = df.iloc[:,[0,1,2,3,4]]
observations = observations.rename(columns=observations.iloc[0]).drop(observations.index[0])
observations.columns.values[0] = 'Period'
observations.columns.values[1] = 'fatal'
observations.columns.values[2] = 'serious'
observations.columns.values[3] = 'slight'
observations.columns.values[4] = 'total'
Final_table = pd.melt(observations,
                       ['Period'], var_name="Severity",
                       value_name="Value")
Final_table['Unit'] = 'accidents'
Final_table['Measure Type'] = 'Count of accidents'
table = pd.concat([table,Final_table])


# In[5]:


observations1 = df.iloc[:,[0,7,9,10,11]]
observations1 = observations1.rename(columns=observations1.iloc[0]).drop(observations1.index[0])
observations1.columns.values[0] = 'Period'
observations1.columns.values[1] = 'killed'
observations1.columns.values[2] = 'seriously-injured'
observations1.columns.values[3] = 'slightly-injured'
observations1.columns.values[4] = 'total'
Final_table = pd.melt(observations1,
                       ['Period'], var_name="Severity",
                       value_name="Value")
Final_table['Unit'] = 'casualties'
Final_table['Measure Type'] = 'Count of casualties'
table = pd.concat([table,Final_table])


# Now deal with the confidence intervals?

# In[6]:


observations3 = df.iloc[:,[0,6,8]]
observations3 = observations3.rename(columns=observations3.iloc[0]).drop(observations3.index[0])
observations3.columns.values[0] = 'Period'
observations3.columns.values[1] = 'CI Lower'
observations3.columns.values[2] = 'CI Upper'
observations3['Severity'] = 'killed'
table = pd.merge(table, observations3, how = 'left', left_on = ['Period','Severity'],
                      right_on = ['Period', 'Severity'])


# In[7]:


table = table[ ['Period','Severity', 'Measure Type','Value', 'CI Lower', 'CI Upper', 'Unit']]


# In[8]:


table['Period'] = 'year/' + table['Period'].map(str)


# In[9]:


import numpy as np
table['CI Lower'] = table['CI Lower'].map(lambda x:
                            '' if x == ':' else x)
table['CI Upper'] = table['CI Upper'].map(lambda x:
                            '' if x == ':' else x)


# In[10]:


from pathlib import Path

out = Path('out')
out.mkdir(exist_ok=True, parents=True)
table.drop_duplicates().to_csv(out / ('observations.csv'), index = False)


# In[13]:


scraper.dataset.family = 'health'
scraper.dataset.theme = THEME['health-social-care']
with open(out / 'dataset.trig', 'wb') as metadata:
    metadata.write(scraper.generate_trig())
    
csvw = CSVWMetadata('https://gss-cogs.github.io/ref_alcohol/')
csvw.create(out / 'observations.csv', out / 'observations.csv-schema.json')


# In[12]:


table


# In[ ]:





# In[ ]:




