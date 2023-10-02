# Script for turning excel-sheet into database
import numpy as np
import pandas as pd
import math
from datetime import datetime
from db_operations import add_forecast
from db_operations import get_forecast_question
from db_operations import update_forecast

# Read the xlsx file
xls = 'preds.xlsx'
raw = pd.read_excel(xls, 'Open Full')

# Transpose and reset the index
t_df = raw.T
t_df.columns = t_df.iloc[0]
df = t_df[1:]
df.reset_index(inplace=True)

# Since I haven't used resolution criteria up until now, I'll just set these to empty
resolution_criteria = ""

# Loop over all the forecast questions to get the parameters to add to the database
for i in range(0, len(df)):
    short_question = df.iloc[i, 0]
    question = df.iloc[i, 1]
    category = df.iloc[i, 2]
    creation_date = datetime.now().date()
    add_forecast(question, short_question, 
                 category, creation_date, resolution_criteria)
    print(i)

upper_ci = ""
lower_ci = ""
# Loop over all the forecast points to get the parameters needed to add to the database. 
for i in range(0, len(df)):
    forecast_id = i + 1
    for a in range('from prediction to predictions10'):
        if df.iloc[i, a] != None:
            point_forecast = df.iloc[i, a]
            upper_ci = point_forecast + 0.15
            lower_ci = point_forecast - 0.15
            date_added = datetime.now().date()
            update_forecast(forecast_id, point_forecast, upper_ci, lower_ci, date_added)
        else: break
