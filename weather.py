
import config
import requests
from datetime import datetime
import psycopg2


def get_chennai_weather():
    url = "https://api.open-meteo.com/v1/forecast?latitude=13.08&longitude=80.27&current_weather=true"
    response = requests.get(url)
    data = response.json()
    weather = data["current_weather"]
    
    record = { "city":  "chennai",
               "temperature":  weather["temperature"],
               "windspeed" : weather["windspeed"],
               "fetched_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    return record

def save_to_database(record):
    conn = psycopg2.connect(
        host="localhost",
        database="weather_DB",
        user="postgres",
        password=config.DB_PASSWORD
    )
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO weather (city, temperature, windspeed, fetched_at) VALUES (%s, %s, %s, %s)",
        (record["city"], record["temperature"], record["windspeed"], record["fetched_at"])
    )
    
    conn.commit()
    cursor.close()
    conn.close()
    print("Saved to database!")

result = get_chennai_weather()
save_to_database(result)

                   
    
