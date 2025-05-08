import requests
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# Creating the Base class for SQLAlchemy models
Base = declarative_base()

class City(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    latitude = Column(Float)
    longitude = Column(Float)
    country_id = Column(Integer)

    # Relationship to daily_weather_entries
    weather_entries = relationship("DailyWeatherEntry", back_populates="city")


# Defining the DailyWeatherEntry model
class DailyWeatherEntry(Base):
    __tablename__ = 'daily_weather_entries'

    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey('cities.id'))
    date = Column(String)
    min_temp = Column(Float)
    max_temp = Column(Float)
    mean_temp = Column(Float)
    precipitation = Column(Float)

    # Relationship to City
    city = relationship("City", back_populates="weather_entries")


# SQLAlchemy engine and session
DATABASE_URL = 'sqlite:///CIS4044-N-SDI-OPENMETEO-PARTIAL.db'
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# Function to fetch weather data from the Open-Meteo API
def fetch_weather_data(city, lat, lon, start_date, end_date):
    url = "https://archive-api.open-meteo.com/v1/archive?latitude=52.52&longitude=13.41&start_date=2024-12-20&end_date=2025-01-03&daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean,apparent_temperature_max,precipitation_sum&timezone=GMT"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data["daily"]
    else:
        print(f"Error fetching data for {city}: {response.status_code}")
        return None

# Function to get or insert a city into the database
def get_or_insert_city(city_name, lat, lon, country_id):
    city = session.query(City).filter_by(name=city_name).first()
    
    if city:
        return city.id
    else:
        # City does not exist, so create a new one
        new_city = City(name=city_name, latitude=lat, longitude=lon, country_id=country_id)
        session.add(new_city)
        session.commit()
        return new_city.id

# Function to insert weather data into the database
def insert_weather_data(city_name, daily_data, lat, lon, country_id):
    # Get or insert the city and retrieve the city_id
    city_id = get_or_insert_city(city_name, lat, lon, country_id)

    for i in range(len(daily_data["time"])):
        new_weather_entry = DailyWeatherEntry(
            city_id=city_id,
            date=daily_data["time"][i],
            min_temp=daily_data["temperature_2m_min"][i],
            max_temp=daily_data["temperature_2m_max"][i],
            mean_temp=daily_data["temperature_2m_mean"][i],
            precipitation=daily_data["precipitation_sum"][i]
        )
        session.add(new_weather_entry)

    session.commit()

# List of cities to fetch weather data for, including their latitude and longitude
cities = [
    {"city": "Berlin", "lat": 52.54833, "lon": 13.407822, "country_id": 3},  
    {"city": "Munich", "lat": 48.1351, "lon": 11.5820, "country_id": 3},  
]

start_date = "2024-11-26"
end_date = "2024-12-10"

# Fetch and insert weather data for each city
for city in cities:
    print(f"Fetching data for {city['city']}...")
    daily_data = fetch_weather_data(city["city"], city["lat"], city["lon"], start_date, end_date)
    
    if daily_data:
        print(f"Inserting data for {city['city']}...")
        insert_weather_data(city["city"], daily_data, city["lat"], city["lon"], city["country_id"])
        print(f"Data for {city['city']} inserted successfully!")

# Function to print all weather data from the database
def print_weather_data():
    weather_entries = session.query(DailyWeatherEntry).all()
    
    for entry in weather_entries:
        print(f"City ID: {entry.city_id}, Date: {entry.date}, Min Temp: {entry.min_temp}, Max Temp: {entry.max_temp}, Mean Temp: {entry.mean_temp}, Precipitation: {entry.precipitation}")

#Print all weather data from the database
print_weather_data()

# Close the session after use
session.close()
