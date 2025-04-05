from application.process_weather import get_all_weather_info

def main():
    country = input("Country: ")
    date = input("Date in YYYY-MM-DD format: ")

    print(get_all_weather_info(country, date))