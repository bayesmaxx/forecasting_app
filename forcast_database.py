import sqlite3 

# Initialize the database
def create_tables():
    with sqlite3.connect('forecasts.db') as conn:
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS forecasts (id INTEGER PRIMARY KEY AUTOINCREMENT, question TEXT, 
                short_question TEXT, category TEXT, creation_date DATETIME, resolution_criteria TEXT)''') 

        cursor.execute('''CREATE TABLE IF NOT EXISTS forecast_points (update_id INTEGER PRIMARY KEY AUTOINCREMENT, forecast_id INTEGER,
                point_forecast REAL, upper_ci REAL, lower_ci REAL, reason TEXT, date_added DATETIME, 
                FOREIGN KEY(forecast_id) REFERENCES forecasts(id))''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS resolutions (id INTEGER PRIMARY KEY AUTOINCREMENT, forecast_id INTEGER,
                resolution TEXT, resolution_date DATETIME, brier_score REAL, 
                logn_score REAL, log2_score REAL, 
               FOREIGN KEY(forecast_id) REFERENCES forecasts(id))''')

