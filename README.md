# Weather Application Project 🌦️

## Overview
In this project, I created a Python-based weather application that integrates **geocoding**, **weather data retrieval**, and **database management**. The application is designed to track and store **historical weather data** for various cities and countries using **SQLite**, **Tkinter** (for GUI), and the **Open-Meteo API**. 🗺️📊

![](rain.gif)

## What Was Performed 🔨

### 1. **Database Setup** 🏗️
I started by setting up an **SQLite database** to store weather-related data. The database includes several tables for **countries**, **cities**, and **daily weather entries**. The goal was to create an efficient and scalable database to store weather data for future queries. 🗃️

### 2. **Fetching Weather Data** 🌤️
I connected to the **Open-Meteo API** to fetch real-time weather data. Using this API, we retrieved data like temperature, precipitation, and other weather-related statistics for various cities. 🌍

### 3. **Storing Data in the Database** 💾
The weather data fetched from the API was stored in the SQLite database for future querying. This helped maintain a **historical record** of weather data over time. 🌦️

### 4. **Data Retrieval** 🔍
Using SQL queries, I fetched weather data from the SQLite database. This data was analyzed to calculate important metrics like:
- **Average Annual Temperature** for cities 🌡️
- **7-Day Precipitation** for specific cities 🌧️
- **Average Mean Temperature** by city 🌞
- **Average Annual Precipitation** for countries 🌍

### 5. **Data Analysis & Calculation** 📈
I performed several analyses on the weather data, such as:
- Calculating **average annual temperature** for specific cities. ❄️
- Finding **average 7-day precipitation** for cities over a given period. 🌧️
- Determining **average mean temperature** for cities within specific date ranges. 🌡️
- Calculating **average annual precipitation** for countries. 🌦️

### 6. **Graphical User Interface (GUI) Development** 🖥️
I created a **GUI application** using **Tkinter** that allows users to easily query the weather data. The interface was built to display the weather data in a user-friendly format, allowing users to:
- **Fetch all countries** 🌍
- **Fetch all cities** 🏙️
- **View average annual temperature** for a given city 🌡️
- **Display 7-day precipitation averages** 🌧️

### 7. **Data Visualization** 📊
In **Phase 2**, I extended the project by adding **data visualization** features. Using the **matplotlib** library, we created several types of charts, such as:
- **Bar Charts** 📊
- **Line Charts** 📈
- **Pie Charts** 🍰

This allowed users to visualize trends in temperature and precipitation across different cities and countries. 🔄

### 8. **Handling Errors and Troubleshooting** ⚠️
Throughout the project, I ensured proper error handling for various issues like:
- **API Errors**: Ensuring the Open-Meteo API responds correctly. 🌐
- **Database Errors**: Making sure the SQLite database is accessible and contains the necessary tables. 🗄️
- **Missing Packages**: Installing missing dependencies like **requests** and **matplotlib** using pip. ⚙️

### 9. **Geocoding** 🌍
I used the **geocoder** library to retrieve the latitude and longitude of cities, helping with the accurate retrieval of weather data for specific locations. 📍

### 10. **SQLAlchemy Integration** 🛠️
I integrated **SQLAlchemy** for **ORM-based database management**, making it easier to interact with the database and handle the weather data using a more structured approach. 🖧

### 11. **Insertion and Retrieval from Database** 💡
I created scripts for:
- **Inserting weather data** into the database after retrieving it from the API.
- **Querying** and **retrieving** historical weather data from the database. 🔄

### 12. **Deployment & Execution** ⚡
I packaged all the scripts and ensured that the entire project could be easily run through terminal commands or an IDE:
```bash
python GUI.py
