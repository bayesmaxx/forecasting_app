import sqlite3
from datetime import datetime 
import math
import numpy as np

# Defining the brier score
def brier_score(point, actual):
    return np.average((point - actual) ** 2)

# Defining the natural logarithm score    
def logn_score(point, actual):
    return np.average(actual * np.log(point) + (1-actual) * np.log(1-point))

# Defining the base 2 log score
def log2_score(point, actual):
    return np.average(actual * np.log2(point) + (1-actual) * np.log2(1-point))

#Function to add a new forecast, the parent table
def add_forecast(question, short_question, category, creation_date, resolution_criteria):
    with sqlite3.connect('forecasts.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO forecasts (question, short_question, category, creation_date, resolution_criteria) 
                       VALUES (?, ?, ?, ?, ?)''', (question, short_question, category, creation_date, resolution_criteria))

# Function to update a forecast
def update_forecast(forecast_id, point_forecast, upper_ci, lower_ci, date_added):
    with sqlite3.connect('forecasts.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO forecast_points (forecast_id, point_forecast, upper_ci, lower_ci, date_added) 
                       VALUES (?, ?, ?, ?, ?)''', (forecast_id, point_forecast, upper_ci, lower_ci, date_added))

# Function to resolve a question
def resolve(forecast_id, resolution, resolution_date):
    with sqlite3.connect('forecasts.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT point_forecast FROM point_forecasts WHERE id=?', (forecast_id))
        forecast_points = cursor.fetchall()
    actual = resolution 
    points = np.array([x for x in forecast_points if isinstance(x, (int, float))])
    # HERE: use the points to get an nparray
    # Define the brier score calculation
    brier_score(points, actual)

# Function to get forecast
def get_forecast(forecast_id):
    with sqlite3.connect('forecasts.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM forecasts WHERE id=?", (forecast_id))
        return cursor.fetchone()
    


