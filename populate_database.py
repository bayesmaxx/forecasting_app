# Script for turning excel-sheet into database
import numpy as np
import pandas as pd
import math
from datetime import datetime
from db_operations import add_forecast

xls = 'preds.xlsx'
raw = pd.read_excel(xls, 'Open Full')

raw.head()

t_df = raw.T
t_df.columns = t_df.iloc[0]
df = t_df[1:]
df.head()
df.reset_index(inplace=True)
df.iloc[:, 0]
short_question = 
t_df[1, 1] 
t_df[1:2]
resolution_criteria = ""

for i in range(0, len(df)):
    short_question = df.iloc[i, 0]
    question = df.iloc[i, 1]
    category = df.iloc[i, 2]
    creation_date = datetime.now().date()
    add_forecast(question, short_question, 
                 category, creation_date, resolution_criteria)
    print(i)