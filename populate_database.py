# Script for turning excel-sheet into database
import numpy as np
import pandas as pd
import math
from datetime import datetime
from db_operations import add_forecast, get_forecast_question, update_forecast, resolve_forecast

# Read the xlsx file
xls = 'preds.xlsx'
sheets = ['Open Full', 'Open Metaculus', 'Finished Full', 'Finished Metaculus']

pre = pd.read_excel(xls, sheets[0])
t_pre = pre.T
t_pre.columns = t_pre.iloc[0]
df = t_pre[1:]
df.reset_index(inplace=True)


for sheet in range(1, len(sheets)):
    pre = pd.read_excel(xls, sheets[sheet])
    t_pre = pre.T
    t_pre.columns = t_pre.iloc[0]
    data = t_pre[1:]
    data.reset_index(inplace=True)
    df.concat(data)    

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
# Unfortunately this is nothing that I've tracked before
date_added = datetime.now().date()
# Loop over all the forecast points to get the parameters needed to add to the database. 
for point in range(0, len(df)):
    forecast_id = point + 1
    for a in range(5, 16):
        if df.iloc[point, a].isnull():
            break
        else:
            point_forecast = df.iloc[point, a]
            upper_ci = point_forecast + 0.15
            lower_ci = point_forecast - 0.15
            update_forecast(forecast_id, point_forecast, upper_ci, lower_ci, date_added)

    if df.iloc[point, 4].is_integer():
        resolution = df.iloc[i, 4]
        resolve_forecast(forecast_id, resolution, date_added)
