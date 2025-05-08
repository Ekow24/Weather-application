import sqlite3

# Function to fetch all countries
def select_all_countries(connection):
    try:
        query = "SELECT * FROM countries"
        cursor = connection.cursor()  
        cursor.execute(query)
        for row in cursor.fetchall():
            print(f"Country Id: {row['id']} -- Country Name: {row['name']} -- Country Timezone: {row['timezone']}")
        cursor.close()  
    except sqlite3.OperationalError as ex:
        print(f"Error executing query: {ex}")

# Function to fetch all cities
def select_all_cities(connection):
    try:
        query = "SELECT * FROM cities"
        cursor = connection.cursor()  
        cursor.execute(query)
        for row in cursor.fetchall():
            print(f"City ID: {row['id']}, City Name: {row['name']}, longitude: {row['longitude']}, latitude: {row['latitude']}, Country ID: {row['country_id']}")
        cursor.close() 
    except sqlite3.OperationalError as ex:
        print(f"Error executing query: {ex}")

# Function to calculate average annual temperature for a specific city and year
def average_annual_temperature(connection, city_id, year):
    try:
        query = """
        SELECT c.name AS city_name, AVG(d.mean_temp) AS avg_temp
        FROM daily_weather_entries d
        JOIN cities c ON d.city_id = c.id
        WHERE d.city_id = ? AND strftime('%Y', d.date) = ?
        GROUP BY c.name
        """
        cursor = connection.cursor() 
        cursor.execute(query, (city_id, str(year)))
        result = cursor.fetchone()
        if result:
            print(f"The Average Annual Temperature for city {result['city_name']} in {year}: {round(result['avg_temp'], 2)} degrees Celsius")
        cursor.close()  
    except sqlite3.OperationalError as ex:
        print(f"Error executing query: {ex}")

# Function to calculate average 7-day precipitation for a specific city and start date
def average_seven_day_precipitation(connection, city_id, start_date):
    try:
        query = """
        SELECT c.name AS city_name, AVG(d.precipitation) AS avg_precip
        FROM daily_weather_entries d
        JOIN cities c ON d.city_id = c.id
        WHERE d.city_id = ? AND d.date >= date(?, '-7 day')
        GROUP BY c.name
        """
        cursor = connection.cursor()  
        cursor.execute(query, (city_id, start_date))
        result = cursor.fetchone()
        if result:
            print(f"Average 7-Day Precipitation for city {result['city_name']}, starting from {start_date}: {round(result['avg_precip'], 2)} mm")
        cursor.close()  
    except sqlite3.OperationalError as ex:
        print(f"Error executing query: {ex}")

# Function to calculate average mean temperature by city within a date range
def average_mean_temp_by_city(connection, date_from, date_to):
    try:
        query = """
        SELECT c.name AS city_name, AVG(d.mean_temp) AS avg_temp
        FROM daily_weather_entries d
        JOIN cities c ON d.city_id = c.id
        WHERE d.date BETWEEN ? AND ?
        GROUP BY c.name
        """
        cursor = connection.cursor()  
        cursor.execute(query, (date_from, date_to))
        for row in cursor.fetchall():
            print(f"Average Mean Temperature for city: {row['city_name']} from {date_from} to {date_to}: {round(row['avg_temp'], 2)} degrees Celsius")
        cursor.close()  
    except sqlite3.OperationalError as ex:
        print(f"Error executing query: {ex}")

# Function to calculate average annual precipitation by country
def average_annual_precipitation_by_country(connection, year):
    try:
        query = """
        SELECT co.name AS country_name, AVG(d.precipitation) AS avg_precip
        FROM cities ci
        JOIN countries co ON ci.country_id = co.id
        JOIN daily_weather_entries d ON ci.id = d.city_id
        WHERE strftime('%Y', d.date) = ?
        GROUP BY co.name
        """
        cursor = connection.cursor()  
        cursor.execute(query, (str(year),))
        for row in cursor.fetchall():
            print(f"Average Annual Precipitation for country: {row['country_name']} in {year}: {round(row['avg_precip'], 2)} mm")
        cursor.close()  
    except sqlite3.OperationalError as ex:
        print(f"Error executing query: {ex}")

# Main function to execute all the tasks
if __name__ == "__main__":
    try:
        # Open connection to the correct database
        with sqlite3.connect('CIS4044-N-SDI-OPENMETEO-PARTIAL.db') as connection:
            connection.row_factory = sqlite3.Row  
           
            print("\nAll Countries:")
            select_all_countries(connection)

            print("\nAll Cities:")
            select_all_cities(connection)

            print("\nAverage Annual Temperature:")
            average_annual_temperature(connection, 1, 2020)

            print("\nAverage 7-Day Precipitation:")
            average_seven_day_precipitation(connection, 1, '2020-12-01')

            print("\nAverage Mean Temperature by City:")
            average_mean_temp_by_city(connection, '2020-01-01', '2020-12-13')

            print("\nAverage Annual Precipitation by Country:")
            average_annual_precipitation_by_country(connection, 2020)

    except sqlite3.Error as ex:
        print(f"Error connecting to database: {ex}")

