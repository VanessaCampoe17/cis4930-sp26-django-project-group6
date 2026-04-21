from django.core.management.base import BaseCommand
import requests
import pandas as pd

# Models lead please create City and WeatherRecord models named exactly that for fetch_data.py to work
from myapp.models import City, WeatherRecord

CITIES = [
    {"name": "Tallahassee", "lat": 30.455, "lon": -84.253},
    {"name": "Miami", "lat": 25.774, "lon": -80.194},
    {"name": "Orlando", "lat": 28.538, "lon": -81.379},
]

class Command(BaseCommand):
    help = 'Fetch weather data from Open-Meteo'
    
    def handle(self, *args, **options):
        df = fetch_multiple_cities(CITIES)
        
        for _, row in df.iterrows():
            city_obj, _ = City.objects.get_or_create(name=row["city"])
            
            WeatherRecord.objects.update_or_create(
                city=city_obj,
                date=row["date"],
                defaults={
                    "temperature_max": row["temperature_max"],
                    "temperature_min": row["temperature_min"],
                    "precipitation": row["precipitation"],
                }
            )
        self.stdout.write(self.style.SUCCESS("Data loaded"))

def fetch_weather(city, lat, lon):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum" , 
        ],
        "timezone": "America/New_York",
    }

    #Section 4.3 Requirement: check timeout and raise for status
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        daily = data.get("daily", {})

        df = pd.DataFrame({
            "city": city,
            "date": daily.get("time", []),
            "temperature_max": daily.get("temperature_2m_max", []),
            "temperature_min": daily.get("temperature_2m_min", []),
            "precipitation": daily.get("precipitation_sum", []),
        })

        return df
    except requests.exceptions.Timeout:
        print(f"TIMEOUT: Cout not fetch API for {city}")
    except requests.exceptions.RequestException as e:
        print(f"REQUEST ERROR for {city}: {e}")

    return pd.DataFrame()

#testing: print(fetch_weather("Tallahassee", 30.455, -84.253334))

#4.4 Pagination
def fetch_multiple_cities(city_list):
    #loop over multiple cities
    all_cities = []

    for city_info in city_list:
        print(f"Fetch: {city_info['name']}...")
        #repeat calls to the API function
        city_df = fetch_weather(city_info['name'], city_info['lat'], city_info['lon'])

        #append data 
        if not city_df.empty:
            all_cities.append(city_df)

    if all_cities:
        return pd.concat(all_cities, ignore_index = True)
    return pd.DataFrame()

