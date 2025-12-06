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



# ⭐ NEW FUNCTION (historical climate fallback)
def get_historical_climate(lat, lon, start_date, end_date):
    """Fetch historical climate averages using Open-Meteo."""
    
    url = "https://climate-api.open-meteo.com/v1/climate"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "daily": "temperature_2m_max_mean,temperature_2m_min_mean,precipitation_sum_mean",
        "models": "ERA5"
    }

    resp = requests.get(url, params=params)
    daily = resp.json().get("daily", {})

    daily_weather = []
    temps = []

    for i, date_str in enumerate(daily.get("time", [])):
        tmax = daily["temperature_2m_max_mean"][i]
        tmin = daily["temperature_2m_min_mean"][i]
        rain = daily["precipitation_sum_mean"][i]

        temps.append(tmax)

        daily_weather.append({
            "date": date_str,
            "tmin": round(tmin, 1),
            "tmax": round(tmax, 1),
            "rain": round(rain, 1),
            "pop": 0       # climate data has no POP
        })

    avg_temp_max = round(sum(temps) / len(temps), 1) if temps else None

    return {
        "daily": daily_weather,
        "avg_temp_max": avg_temp_max,
        "max_pop": 0
    }



# ⭐ MODIFY YOUR EXISTING FUNCTION (no deletions)
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
            rain_mm = day.get("rain", 0)   # ⭐ NEW

            temps.append(tmax)
            max_pop = max(max_pop, pop)

            daily_weather.append({
                "date": dt.isoformat(),
                "tmin": tmin,
                "tmax": tmax,
                "rain": rain_mm,   # ⭐ NEW
                "pop": pop
            })

    # ⭐ NEW: if no forecast available, fallback to historical climate
    if not daily_weather:
        return get_historical_climate(lat, lon, start_date, end_date)

    avg_temp_max = round(sum(temps) / len(temps), 1) if temps else None

    return {
        "daily": daily_weather,
        "avg_temp_max": avg_temp_max,
        "max_pop": max_pop
    }
