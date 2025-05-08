import requests
import sqlite3
from datetime import datetime

# Define the function to retrieve weather data from Open-Meteo API
def fetch_weather_data(city, lat, lon, start_date, end_date):
    try:
        url = "https://archive-api.open-meteo.com/v1/archive?latitude=52.52&longitude=13.41&start_date=2024-12-20&end_date=2025-01-03&daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean,apparent_temperature_max,precipitation_sum&timezone=GMT"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            return data["daily"]
        else:
            print(f"Error fetching data for {city}: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"An error occurred while fetching weather data for {city}: {e}")
        return None

# Function to get the city_id from the cities table, or insert the city if it does not exist
def get_or_insert_city(city_name, lat, lon, country_id, conn):
    try:
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM cities WHERE name = ?", (city_name,))
        city_id = cursor.fetchone()
        
        if city_id:
            # City exists, return the city_id
            return city_id[0]
        else:
            # City does not exist, insert it into the cities table
            cursor.execute(''' 
                INSERT INTO cities (name, latitude, longitude, country_id)
                VALUES (?, ?, ?, ?)
            ''', (city_name, lat, lon, country_id))
            conn.commit()
            
            # Fetch and return the newly inserted city_id
            cursor.execute("SELECT id FROM cities WHERE name = ?", (city_name,))
            city_id = cursor.fetchone()
            return city_id[0]
    except sqlite3.DatabaseError as e:
        print(f"Database error occurred while handling city {city_name}: {e}")
        return None

# Function to insert weather data into the database
def insert_weather_data(city_name, daily_data, lat, lon, country_id):
    try:
        with sqlite3.connect('CIS4044-N-SDI-OPENMETEO-PARTIAL.db') as conn:
            cursor = conn.cursor()

            # Get or insert the city and retrieve the city_id
            city_id = get_or_insert_city(city_name, lat, lon, country_id, conn)

            if city_id is None:
                print(f"Failed to retrieve or insert city {city_name}. Skipping weather data insertion.")
                return

            # Insert each day's data into the database
            data_to_insert = [
                (city_id, daily_data["time"][i], daily_data["temperature_2m_min"][i], 
                 daily_data["temperature_2m_max"][i], daily_data["temperature_2m_mean"][i],
                 daily_data["precipitation_sum"][i])
                for i in range(len(daily_data["time"]))
            ]

            cursor.executemany('''
                INSERT INTO daily_weather_entries (city_id, date, min_temp, max_temp, mean_temp, precipitation)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', data_to_insert)

            conn.commit()
    except sqlite3.DatabaseError as e:
        print(f"Database error occurred while inserting weather data: {e}")
    except Exception as e:
        print(f"An error occurred while inserting weather data for {city_name}: {e}")

# List of cities to fetch data for, including their latitude and longitude
cities = [
    {"city": "Berlin", "lat": 52.54833, "lon": 13.407822, "country_id": 3},  
    {"city": "Munich", "lat": 48.1351, "lon": 11.5820, "country_id": 3},  
]

start_date = "2024-11-26"
end_date = "2024-12-10"

# Fetch and insert data for each city
for city in cities:
    try:
        print(f"Fetching data for {city['city']}...")
        daily_data = fetch_weather_data(city["city"], city["lat"], city["lon"], start_date, end_date)
        
        if daily_data:
            print(f"Inserting data for {city['city']}...")
            insert_weather_data(city["city"], daily_data, city["lat"], city["lon"], city["country_id"])
            print(f"Data for {city['city']} inserted successfully!")
    except Exception as e:
        print(f"An error occurred while processing data for {city['city']}: {e}")

# Function to print all data from the database
def print_weather_data():
    try:
        with sqlite3.connect('CIS4044-N-SDI-OPENMETEO-PARTIAL.db') as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM daily_weather_entries") 
            rows = cursor.fetchall()

            for row in rows:
                print(row)
    except sqlite3.DatabaseError as e:
        print(f"Database error occurred while printing weather data: {e}")
    except Exception as e:
        print(f"An error occurred while printing weather data: {e}")
