# Script for turning excel-sheet into database
import numpy as np
import pandas as pd
import math
from datetime import datetime
from db_operations import add_forecast, update_forecast, resolve_forecast
from forcast_database import create_tables


create_tables()
# Read the xlsx file
xls = '/Users/samuelsvensson/Documents/forecasting_data/preds.xlsx'


pre = pd.read_excel(xls, 'Open Full')
t_pre = pre.T
t_pre.columns = t_pre.iloc[0]
df = t_pre[1:]
df.reset_index(inplace=True)

# Since I haven't used resolution criteria up until now, I'll just set these to empty
resolution_criteria = ""
creation_date = datetime.now().date()
# Loop over all the forecast questions to get the parameters to add to the database
for i in range(0, len(df)):
    short_question = df.iloc[i, 0]
    question = df.iloc[i, 1]
    category = df.iloc[i, 2]
    add_forecast(question, short_question, 
                 category, creation_date, resolution_criteria)

# Unfortunately this is nothing that I've tracked before
upper_ci = ""
lower_ci = ""
date_added = datetime.now().date()
reason = ""

# Loop over all the forecast points to get the parameters needed to add to the database. 
for point in range(0, len(df)):
    forecast_id = point + 1
    for a in range(5, 16):
        if not np.isnan(df.iloc[point, a]):
            point_forecast = df.iloc[point, a]
            upper_ci = max(point_forecast + 0.15, 1)
            lower_ci = max(point_forecast - 0.15, 0)
            update_forecast(forecast_id, point_forecast, upper_ci, lower_ci, reason, date_added)
        else: 
            break
            
    if not np.isnan(df.iloc[point, 4]):
        resolution = df.iloc[point, 4]
        resolve_forecast(forecast_id, resolution, date_added)

