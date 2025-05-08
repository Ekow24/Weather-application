import requests
import sqlite3
import geocoder
from datetime import datetime

# Define the function to retrieve data from Open-Meteo API
def fetch_weather_data(city, lat, lon, start_date, end_date):
    url = "https://archive-api.open-meteo.com/v1/archive?latitude=52.52&longitude=13.41&start_date=2024-12-20&end_date=2025-01-03&daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean,apparent_temperature_max,precipitation_sum&timezone=GMT"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()  
        return data["daily"]
    else:
        print(f"Error fetching data for {city}: {response.status_code}")
        return None

# Function to get the city_id from the cities table, or insert the city if it does not exist
def get_or_insert_city(city_name, lat, lon, country_id, conn):
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

# Function to insert data into the database
def insert_weather_data(city_name, daily_data, lat, lon, country_id):
    with sqlite3.connect('CIS4044-N-SDI-OPENMETEO-PARTIAL.db') as conn:
        cursor = conn.cursor()

        # Get or insert the city and retrieve the city_id
        city_id = get_or_insert_city(city_name, lat, lon, country_id, conn)

        # Inserting each day's data into the database
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

# Function to get latitude and longitude of a city using geocoder
def get_lat_lon_from_city(city_name):
    g = geocoder.arcgis(city_name)  
    
    if g.ok:
        return g.latlng
    else:
        print(f"Error: Could not geocode city '{city_name}'")
        return None

# List of cities to fetch data for (without lat, lon as they will be fetched dynamically)
cities = [
    {"city": "Berlin", "country_id": 3},  
    {"city": "Munich", "country_id": 3},  
]

start_date = "2024-11-26"
end_date = "2024-12-10"

# Fetch and insert data for each city
for city in cities:
    print(f"Fetching latitude and longitude for {city['city']}...")
    lat_lon = get_lat_lon_from_city(city["city"])
    
    if lat_lon:
        lat, lon = lat_lon
        print(f"Fetching weather data for {city['city']}...")
        daily_data = fetch_weather_data(city["city"], lat, lon, start_date, end_date)
        
        if daily_data:
            print(f"Inserting data for {city['city']}...")
            insert_weather_data(city["city"], daily_data, lat, lon, city["country_id"])
            print(f"Data for {city['city']} inserted successfully!")
        else:
            print(f"Failed to fetch weather data for {city['city']}")
    else:
        print(f"Skipping {city['city']} due to geocoding failure.")

# Function to print all weather data from the database
def print_weather_data():
    with sqlite3.connect('CIS4044-N-SDI-OPENMETEO-PARTIAL.db') as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM daily_weather_entries") 
        rows = cursor.fetchall()

        for row in rows:
            print(row)
