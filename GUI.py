import sqlite3
import tkinter as tk
from tkinter import messagebox, scrolledtext

# Function to fetch all countries
def select_all_countries(connection):
    try:
        query = "SELECT * FROM countries"
        cursor = connection.cursor()
        cursor.execute(query)
        result = ""
        for row in cursor.fetchall():
            result += f"Country Id: {row['id']} -- Country Name: {row['name']} -- Country Timezone: {row['timezone']}\n"
        cursor.close()
        return result if result else "No countries found."
    except sqlite3.OperationalError as ex:
        return f"Error executing query: {ex}"

# Function to fetch all cities
def select_all_cities(connection):
    try:
        query = "SELECT * FROM cities"
        cursor = connection.cursor()
        cursor.execute(query)
        result = ""
        for row in cursor.fetchall():
            result += f"City ID: {row['id']}, City Name: {row['name']}, Longitude: {row['longitude']}, Latitude: {row['latitude']}, Country ID: {row['country_id']}\n"
        cursor.close()
        return result if result else "No cities found."
    except sqlite3.OperationalError as ex:
        return f"Error executing query: {ex}"

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
        cursor.close()
        if result:
            return f"The Average Annual Temperature for city {result['city_name']} in {year}: {round(result['avg_temp'], 2)} degrees Celsius"
        return "No data found for this city and year."
    except sqlite3.OperationalError as ex:
        return f"Error executing query: {ex}"

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
        cursor.close()
        if result:
            return f"Average 7-Day Precipitation for city {result['city_name']}, starting from {start_date}: {round(result['avg_precip'], 2)} mm"
        return "No data found for this city and date range."
    except sqlite3.OperationalError as ex:
        return f"Error executing query: {ex}"

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
        result = ""
        for row in cursor.fetchall():
            result += f"Average Mean Temperature for city {row['city_name']} from {date_from} to {date_to}: {round(row['avg_temp'], 2)} degrees Celsius\n"
        cursor.close()
        return result if result else "No data found in this date range."
    except sqlite3.OperationalError as ex:
        return f"Error executing query: {ex}"

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
        result = ""
        for row in cursor.fetchall():
            result += f"Average Annual Precipitation for country {row['country_name']} in {year}: {round(row['avg_precip'], 2)} mm\n"
        cursor.close()
        return result if result else "No data found for this year."
    except sqlite3.OperationalError as ex:
        return f"Error executing query: {ex}"

# Main GUI Function
def create_gui():
    def show_result(query_func, *args):
        try:
            with sqlite3.connect('CIS4044-N-SDI-OPENMETEO-PARTIAL.db') as connection:
                connection.row_factory = sqlite3.Row  # Ensure rows are returned as dictionaries
                result = query_func(connection, *args)
                output_text.delete(1.0, tk.END)
                output_text.insert(tk.END, result)
        except sqlite3.Error as ex:
            messagebox.showerror("Database Error", f"Error connecting to database: {ex}")

    window = tk.Tk()
    window.title("Weather Data GUI")

    # Text area to display results
    output_text = scrolledtext.ScrolledText(window, width=80, height=20)
    output_text.pack(padx=10, pady=10)

    # Buttons for each function
    btn_countries = tk.Button(window, text="All Countries", command=lambda: show_result(select_all_countries))
    btn_countries.pack(pady=5)

    btn_cities = tk.Button(window, text="All Cities", command=lambda: show_result(select_all_cities))
    btn_cities.pack(pady=5)

    btn_temp = tk.Button(window, text="Average Annual Temperature", command=lambda: show_result(average_annual_temperature, 1, 2020))
    btn_temp.pack(pady=5)

    btn_precip = tk.Button(window, text="Average 7-Day Precipitation", command=lambda: show_result(average_seven_day_precipitation, 1, '2020-12-01'))
    btn_precip.pack(pady=5)

    btn_mean_temp = tk.Button(window, text="Average Mean Temperature by City", command=lambda: show_result(average_mean_temp_by_city, '2020-01-01', '2020-12-13'))
    btn_mean_temp.pack(pady=5)

    btn_precip_country = tk.Button(window, text="Average Annual Precipitation by Country", command=lambda: show_result(average_annual_precipitation_by_country, 2020))
    btn_precip_country.pack(pady=5)

    window.mainloop()

# Run the GUI
if __name__ == "__main__":
    create_gui()

