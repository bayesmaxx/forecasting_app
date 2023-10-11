# File for adding some new forecasts as well as updating some old ones
from db_operations import add_forecast, update_forecast, resolve_forecast
from datetime import datetime

creation_date = datetime.now().date()
while True:
    action = input("Would you like to 'add' a new forecast or 'update' or 'resolve' an existing one? (Type 'exit' to quit): ")
    
    if action == "add":
        question = input("Enter the question: ")
        short_question = input("Enter the short question: ")
        category = input("Enter the category: ")
        resolution_criteria = input("Enter the resolution criteria: ")
        
        add_forecast(question, short_question, category, creation_date, resolution_criteria)
        
    elif action == "update":
        forecast_id = int(input("Enter the forecast ID: "))
        point_forecast = float(input("Enter the point forecast: "))
        upper_ci = float(input("Enter the upper CI: "))
        lower_ci = float(input("Enter the lower CI: "))
        reason = input("Enter the reason for update: ")
        
        update_forecast(forecast_id, point_forecast, upper_ci, lower_ci, reason, creation_date)
    
    elif action == "resolve":
        forecast_id2 = int(input("Enter the forecast ID: "))
        res = input("Did the question resolve as 'yes' or 'no': ")
        if res == "yes":
            resolution = 1
        elif res == "no":
            resolution = 0
        else:
            print("Invalid input. Try again")
            break
        resolve_forecast(forecast_id2, resolution, creation_date)
    elif action == "exit":
        break
    else:
        print("Invalid action. Try again.")