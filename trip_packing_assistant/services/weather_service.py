import requests
from datetime import datetime
from config import Config


def get_coordinates(city_name):
    """Use OpenWeather geocoding to convert city → lat/lon"""
    url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {
        "q": city_name,
        "limit": 1,
        "appid": Config.OPENWEATHER_API_KEY
    }

    resp = requests.get(url, params=params)
    data = resp.json()

    if not data:
        return None, None

    return data[0]["lat"], data[0]["lon"]


def get_trip_weather(lat, lon, start_date, end_date):
    """Fetch daily forecast from OpenWeather OneCall API"""

    url = "https://api.openweathermap.org/data/3.0/onecall"
    params = {
        "lat": lat,
        "lon": lon,
        "exclude": "minutely,hourly,alerts",
        "units": "metric",
        "appid": Config.OPENWEATHER_API_KEY
    }

    resp = requests.get(url, params=params)
    raw = resp.json().get("daily", [])

    daily_weather = []
    temps = []
    max_pop = 0

    for day in raw:
        dt = datetime.fromtimestamp(day["dt"]).date()
        if start_date.date() <= dt <= end_date.date():
            tmin = day["temp"]["min"]
            tmax = day["temp"]["max"]
            pop = day.get("pop", 0)

            temps.append(tmax)
            max_pop = max(max_pop, pop)

            daily_weather.append({
                "date": dt.isoformat(),
                "tmin": tmin,
                "tmax": tmax,
                "pop": pop
            })

    avg_temp_max = round(sum(temps) / len(temps), 1) if temps else None

    return {
        "daily": daily_weather,
        "avg_temp_max": avg_temp_max,
        "max_pop": max_pop
    }