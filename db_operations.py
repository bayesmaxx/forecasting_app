import sqlite3
from datetime import datetime
import math
import numpy as np


# Defining the brier score
def brier_score(point, actual):
    return np.mean((point - actual) ** 2)

# Defining the natural logarithm score
def logn_score(point, actual):
    return np.mean(actual * np.log(point) + (1-actual) * np.log(1-point))

# Defining the base 2 log score
def log2_score(point, actual):
    return np.mean(actual * np.log2(point) + (1-actual) * np.log2(1-point))


#Function to add a new forecast, the parent table
def add_forecast(question, short_question, category, creation_date, resolution_criteria):
    with sqlite3.connect('forecasts.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO forecasts (question, short_question, category, creation_date, resolution_criteria)
                        VALUES (?, ?, ?, ?, ?)''', (question, short_question, category, creation_date, resolution_criteria))

# Function to update a forecast
def update_forecast(forecast_id, point_forecast, upper_ci, lower_ci, reason, date_added):
    with sqlite3.connect('forecasts.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO forecast_points (forecast_id, point_forecast, upper_ci, lower_ci, reason, date_added)
                        VALUES (?, ?, ?, ?, ?, ?)''', (forecast_id, point_forecast, upper_ci, lower_ci, reason, date_added))


# Function to resolve a question
def resolve_forecast(forecast_id, resolution, resolution_date):
    with sqlite3.connect('forecasts.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT point_forecast FROM forecast_points WHERE forecast_id=?', (forecast_id, ))
    forecast_points = cursor.fetchall()
    actual = resolution
    points = np.array([point for res in forecast_points for point in res])
# HERE: use the points to get an nparray
# Define the brier score calculation
    brier = brier_score(points, actual)
    log2 = log2_score(points, actual)
    logn = logn_score(points, actual)
    with sqlite3.connect('forecasts.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO resolutions (forecast_id, resolution, resolution_date
                        , brier_score, logn_score, log2_score) VALUES (?,?,?,?,?,?)''',
                        (forecast_id, resolution, resolution_date, brier, logn, log2))

# Function to get information from the forecast table only
def get_forecast_question(forecast_id):
    with sqlite3.connect('forecasts.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM forecasts WHERE id=?", (forecast_id, ))
    return cursor.fetchone()

# Function to get forecast_points information only
def get_forecast_points(forecast_id):
    with sqlite3.connect('forecasts.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM forecast_points WHERE forecast_id=?''', (forecast_id,))
    return cursor.fetchall()


# Function to get the full forecast information, including updates and resolution
def get_full_forecast(forecast_id):
    with sqlite3.connect('forecasts.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT *
                    FROM forecasts AS f
                    LEFT JOIN forecast_points AS f_point
                    ON f.id = f_point.forecast_id
                    LEFT JOIN resolutions AS res
                    ON f.id = res.forecast_id
                    WHERE f.id = ?''', (forecast_id, ))
    return cursor.fetchall()
# The problem here is that for a forecast with 3 updates, this will return three
# separate rows that are equivalent apart from the forecast points data


# Function to delete full forecast with all associated information
def del_forecast(forecast_id):
    with sqlite3.connect('forecast.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''DELETE FROM forecasts WHERE id=?''', (forecast_id, ))
        cursor.execute('''DELETE FROM forecast_points WHERE forecast_id=?''', (forecast_id, ))
        cursor.execute('''DELETE FROM resolutions WHERE forecast_id=?''', (forecast_id, ))


# Function to delete a specific update, NB: this requires knowing the id of the forecast
def del_update(id, forecast_id):
    with sqlite3.connect('forecasts.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''DELETE FROM forecast_points WHERE id=? AND forecast_id=?''', (id, forecast_id))


# Function to just change a specific update, in case of a mistake or similar.
def change_update(id, forecast_id, new_point, new_upper, new_lower):
    with sqlite3.connect('forecasts.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''UPDATE forecast_points SET point_forecast=?, upper_ci=?, lower_ci=?
                        WHERE id=? AND forecast_id=?''', (new_point, new_upper, new_lower, id, forecast_id))
        
# Functions to return the average score
def avg_brier(category=None):
    if category:
        with sqlite3.connect('forecasts.db') as conn:
            cursor = conn.cursor()
            like_query = "%" + category + "%"
            cursor.execute('''SELECT brier_score FROM resolutions AS r LEFT JOIN forecasts AS f ON f.id = r.forecast_id WHERE f.category LIKE ?''', (like_query,))
            scores = cursor.fetchall()
        points = np.array([point for res in scores for point in res])
        return np.mean(points)
    else:
        with sqlite3.connect('forecasts.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT brier_score FROM resolutions''')
            scores = cursor.fetchall()
        points = np.array([point for res in scores for point in res])
        return np.mean(points)

def avg_logn(category=None):
    if category:
        with sqlite3.connect('forecasts.db') as conn:
            cursor = conn.cursor()
            like_query = "%" + category + "%"
            cursor.execute('''SELECT logn_score FROM resolutions AS r LEFT JOIN forecasts AS f ON f.id = r.forecast_id WHERE f.category LIKE ?''', (like_query,))
            scores = cursor.fetchall()
        points = np.array([point for res in scores for point in res])
        return np.mean(points)
    else:
        with sqlite3.connect('forecasts.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT logn_score FROM resolutions''')
            scores = cursor.fetchall()
        points = np.array([point for res in scores for point in res])
        return np.mean(points)

def avg_log2(category=None):
    if category:
        with sqlite3.connect('forecasts.db') as conn:
            cursor = conn.cursor()
            like_query = "%" + category + "%"
            cursor.execute('''SELECT log2_score FROM resolutions AS r LEFT JOIN forecasts AS f ON f.id = r.forecast_id WHERE f.category LIKE ?''', (like_query,))
            scores = cursor.fetchall()
        points = np.array([point for res in scores for point in res])
        return np.mean(points)
    else:
        with sqlite3.connect('forecasts.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT log2_score FROM resolutions''')
            scores = cursor.fetchall()
        points = np.array([point for res in scores for point in res])
        return np.mean(points)