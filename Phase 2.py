import sqlite3
import matplotlib.pyplot as plt

# Function to fetch all countries
def select_all_countries(connection):
    try:
        query = "SELECT * FROM countries"
        cursor = connection.cursor()  
        cursor.execute(query)
        countries = cursor.fetchall()
        cursor.close()  
        return countries
    except sqlite3.OperationalError as ex:
        print(f"Error executing query: {ex}")
        return []

# Function to fetch all cities
def select_all_cities(connection):
    try:
        query = "SELECT * FROM cities"
        cursor = connection.cursor()  
        cursor.execute(query)
        cities = cursor.fetchall()
        cursor.close()  
        return cities
    except sqlite3.OperationalError as ex:
        print(f"Error executing query: {ex}")
        return []

# Function to fetch average precipitation for a given period
def fetch_avg_precipitation_for_period(connection, start_date, end_date):
    query = """
    SELECT AVG(precipitation) AS avg_precipitation
    FROM daily_weather_entries
    WHERE date BETWEEN ? AND ?
    """
    cursor = connection.cursor()
    cursor.execute(query, (start_date, end_date))
    data = cursor.fetchone()
    cursor.close()
    return data[0] if data else None

# Function to fetch min and max temperature for a specific city within a period
def fetch_min_max_temp_for_city(connection, city_name, start_date, end_date):
    query = """
    SELECT MIN(mean_temp) AS min_temp, MAX(mean_temp) AS max_temp
    FROM daily_weather_entries
    WHERE city_id = (SELECT id FROM cities WHERE name = ?) AND date BETWEEN ? AND ?
    """
    cursor = connection.cursor()
    cursor.execute(query, (city_name, start_date, end_date))
    data = cursor.fetchone()
    cursor.close()
    return data if data else (None, None)

# Function to plot average precipitation for a period
def plot_avg_precipitation(period1_data, period2_data):
    labels = ['2020-01-01 to 2020-06-30', '2020-07-01 to 2020-12-31']
    values = [period1_data, period2_data]
    plt.bar(labels, values, color=['blue', 'green'])
    plt.xlabel('Period')
    plt.ylabel('Average Precipitation (mm)')
    plt.title('Average Precipitation for Two Periods')
    plt.xticks(rotation=0)  
    plt.show()

# Function to plot min and max temperatures for a city
def plot_min_max_temp(city_data, city_name):
    min_temps = [city_data[0]]
    max_temps = [city_data[1]]
    
    plt.bar(city_name, min_temps, width=0.4, label='Min Temp (°C)', color='blue', align='center')
    plt.bar(city_name, max_temps, width=0.4, label='Max Temp (°C)', color='red', align='edge')
    plt.xlabel('City')
    plt.ylabel('Temperature (°C)')
    plt.title(f'Min and Max Temperatures for {city_name}')
    plt.legend()
    plt.xticks(rotation=0)  
    plt.show()

# Function to plot the number of cities in each country
def plot_cities_per_country(countries, cities):
    city_count = {country['name']: 0 for country in countries}
    for city in cities:
        country_id = city['country_id']
        for country in countries:
            if country['id'] == country_id:
                city_count[country['name']] += 1

    countries = list(city_count.keys())
    counts = list(city_count.values())

    plt.bar(countries, counts, color='orange')
    plt.xlabel('Country')
    plt.ylabel('Number of Cities')
    plt.title('Number of Cities in Each Country')
    plt.xticks(rotation=0)  
    plt.show()

# Function to plot temperature variations for all cities
def plot_temp_variations_for_all_cities(cities):
    city_names = [city['name'] for city in cities]
    min_temps = []
    max_temps = []

    for city in cities:
        city_data = fetch_min_max_temp_for_city(connection, city['name'], '2020-01-01', '2020-06-30')
        min_temps.append(city_data[0])
        max_temps.append(city_data[1])

    plt.plot(city_names, min_temps, label='Min Temp (°C)', marker='o', color='blue')
    plt.plot(city_names, max_temps, label='Max Temp (°C)', marker='x', color='red')
    plt.xlabel('City')
    plt.ylabel('Temperature (°C)')
    plt.title('Temperature Variations for All Cities')
    plt.xticks(rotation=0)  
    plt.legend()
    plt.show()

# Function to plot the average temperature for all cities
def plot_avg_temp_for_all_cities(cities):
    city_names = [city['name'] for city in cities]
    avg_temps = []

    for city in cities:
        query = """
        SELECT AVG(mean_temp) FROM daily_weather_entries
        WHERE city_id = ?
        """
        cursor = connection.cursor()
        cursor.execute(query, (city['id'],))
        data = cursor.fetchone()
        cursor.close()
        avg_temps.append(data[0] if data[0] is not None else 0)

    plt.bar(city_names, avg_temps, color='purple')
    plt.xlabel('City')
    plt.ylabel('Average Temperature (°C)')
    plt.title('Average Temperature for All Cities')
    plt.xticks(rotation=0)  
    plt.show()

# Function to plot temperature variation across two periods for a city
def plot_temp_variation_for_periods(connection, city_name, period1_start, period1_end, period2_start, period2_end):
    min_temp_period1 = fetch_min_max_temp_for_city(connection, city_name, period1_start, period1_end)[0]
    max_temp_period1 = fetch_min_max_temp_for_city(connection, city_name, period1_start, period1_end)[1]
    min_temp_period2 = fetch_min_max_temp_for_city(connection, city_name, period2_start, period2_end)[0]
    max_temp_period2 = fetch_min_max_temp_for_city(connection, city_name, period2_start, period2_end)[1]

    labels = [f"{city_name} - 2020-01-01 to 2020-06-30", f"{city_name} - 2020-07-01 to 2020-12-31"]
    min_temps = [min_temp_period1, min_temp_period2]
    max_temps = [max_temp_period1, max_temp_period2]

    x = range(len(labels))
    plt.barh(x, min_temps, height=0.4, label='Min Temp (°C)', color='blue', align='center')
    plt.barh(x, max_temps, height=0.4, label='Max Temp (°C)', color='red', align='edge')

    plt.yticks(x, labels, fontsize=8)  
    plt.xlabel('Temperature (°C)')
    plt.ylabel('Period')
    plt.title(f'Temperature Variation for {city_name}')
    plt.legend()
    plt.tight_layout()  
    plt.show()

# Function to add Box Plot for Temperature Variations
def plot_box_plot(cities):
    city_names = [city['name'] for city in cities]
    temperature_data = []

    for city in cities:
        query = """
        SELECT mean_temp FROM daily_weather_entries
        WHERE city_id = ?
        """
        cursor = connection.cursor()
        cursor.execute(query, (city['id'],))
        data = cursor.fetchall()
        cursor.close()
        temps = [entry[0] for entry in data if entry[0] is not None]
        temperature_data.append(temps)

    plt.boxplot(temperature_data, labels=city_names)
    plt.xlabel('City')
    plt.ylabel('Temperature (°C)')
    plt.title('Temperature Distribution for Each City')
    plt.xticks(rotation=0)  
    plt.show()

# Function to add Pie Chart for Distribution of Average Temperatures
def plot_pie_chart(countries, cities):
    city_avg_temps = []
    city_names = []
    
    for city in cities:
        query = """
        SELECT AVG(mean_temp) FROM daily_weather_entries
        WHERE city_id = ?
        """
        cursor = connection.cursor()
        cursor.execute(query, (city['id'],))
        data = cursor.fetchone()
        cursor.close()
        
        avg_temp = data[0] if data[0] is not None else 0
        city_avg_temps.append(avg_temp)
        city_names.append(city['name'])

    plt.pie(city_avg_temps, labels=city_names, autopct='%1.1f%%', startangle=90)
    plt.title('Distribution of Average Temperatures Across Cities')
    plt.axis('equal')  
    plt.show()

# Main function to execute all tasks
if __name__ == "__main__":
    try:
        # Open connection to the database
        with sqlite3.connect('CIS4044-N-SDI-OPENMETEO-PARTIAL.db') as connection:
            connection.row_factory = sqlite3.Row  

            # Fetch data
            countries = select_all_countries(connection)
            cities = select_all_cities(connection)

            # Generate plots
            avg_precip_period1 = fetch_avg_precipitation_for_period(connection, '2020-01-01', '2020-06-30')
            avg_precip_period2 = fetch_avg_precipitation_for_period(connection, '2020-07-01', '2020-12-31')
            plot_avg_precipitation(avg_precip_period1, avg_precip_period2)

            # Plot for specific city temperatures
            city_name = 'Middlesbrough'
            city_temp = fetch_min_max_temp_for_city(connection, city_name, '2020-01-01', '2020-06-30')
            plot_min_max_temp(city_temp, city_name)

            # Plot cities per country
            plot_cities_per_country(countries, cities)

            # Plot temperature variations for all cities
            plot_temp_variations_for_all_cities(cities)

            # Plot average temperature for all cities
            plot_avg_temp_for_all_cities(cities)

            # Plot temperature variation for periods
            plot_temp_variation_for_periods(connection, 'Middlesbrough', '2020-01-01', '2020-06-30', '2020-07-01', '2020-12-31')

            # Plot Box Plot
            plot_box_plot(cities)

            # Plot Pie Chart
            plot_pie_chart(countries, cities)

    except sqlite3.Error as ex:
        print(f"Error connecting to database: {ex}")



