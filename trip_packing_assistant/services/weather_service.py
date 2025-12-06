import requests
from datetime import datetime, timedelta
from config import Config, TEMP_COLD, RAIN_THRESHOLD

def get_coordinates(city_name):
    """Use OpenWeather geocoding to convert city → lat/lon"""
    url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {
        "q": city_name,
        "limit": 1,
        "appid": Config.OPENWEATHER_API_KEY
    }

    try:
        resp = requests.get(url, params=params)
        data = resp.json()
        if not data:
            return None, None
        return data[0]["lat"], data[0]["lon"]
    except Exception:
        return None, None

# ⭐ NEW FUNCTION (historical climate fallback)
def get_historical_climate(lat, lon, start_date, end_date):
    """Fetch historical climate averages using Open-Meteo."""
    
    # FIX: Map future dates to a past year (2022) to get available historical data
    try:
        req_start = start_date.replace(year=2022)
        req_end = end_date.replace(year=2022)
    except ValueError:
        # Handle leap year edge cases
        req_start = start_date.replace(year=2022, day=28)
        req_end = end_date.replace(year=2022, day=28)

    url = "https://climate-api.open-meteo.com/v1/climate"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": req_start.strftime("%Y-%m-%d"),
        "end_date": req_end.strftime("%Y-%m-%d"),
        "daily": "temperature_2m_max_mean,temperature_2m_min_mean,precipitation_sum_mean",
        "models": "ERA5_HRES"
    }

    try:
        resp = requests.get(url, params=params)
        daily = resp.json().get("daily", {})

        daily_weather = []
        temps = []

        # Use the length of the returned data to iterate
        data_length = len(daily.get("temperature_2m_max_mean", []))
        
        # We assume the API returns days in order, matching our requested duration
        current_date_display = start_date

        for i in range(data_length):
            tmax = daily["temperature_2m_max_mean"][i]
            tmin = daily["temperature_2m_min_mean"][i]
            rain = daily["precipitation_sum_mean"][i]

            # Handle possible None values from API
            if tmax is None: tmax = 20.0
            if tmin is None: tmin = 10.0
            if rain is None: rain = 0.0

            temps.append(tmax)

            daily_weather.append({
                "date": current_date_display.strftime("%Y-%m-%d"),
                "tmin": round(tmin, 1),
                "tmax": round(tmax, 1),
                "rain": round(rain, 1),
                "pop": 0,
                "desc": "Historical Average"
            })
            current_date_display += timedelta(days=1)

        avg_temp_max = round(sum(temps) / len(temps), 1) if temps else 20.0

        return {
            "daily": daily_weather,
            "avg_temp_max": avg_temp_max,
            "max_pop": 0,
            "is_cold": avg_temp_max < TEMP_COLD,
            "is_rainy": False
        }
    except Exception as e:
        print(f"Historical API Error: {e}")
        # Ultimate fallback to prevent crash
        return {
            "daily": [], "avg_temp_max": 20.0, "max_pop": 0, 
            "is_cold": False, "is_rainy": False
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

    try:
        resp = requests.get(url, params=params)
        
        # If API fails (e.g., 401 Unauthorized because key isn't enabled for OneCall 3.0), use fallback
        if resp.status_code != 200:
            print("OneCall failed, switching to historical...")
            return get_historical_climate(lat, lon, start_date, end_date)

        raw = resp.json().get("daily", [])
        if not raw:
            return get_historical_climate(lat, lon, start_date, end_date)

        daily_weather = []
        temps = []
        max_pop = 0

        for day in raw:
            dt = datetime.fromtimestamp(day["dt"])

            if start_date.date() <= dt.date() <= end_date.date():
                tmin = day["temp"]["min"]
                tmax = day["temp"]["max"]
                pop = day.get("pop", 0)
                rain_mm = day.get("rain", 0)

                temps.append(tmax)
                max_pop = max(max_pop, pop)

                daily_weather.append({
                    "date": dt.strftime("%Y-%m-%d"),
                    "tmin": tmin,
                    "tmax": tmax,
                    "rain": rain_mm,
                    "pop": pop,
                    "desc": day["weather"][0]["description"]
                })

        # If filtering returned no days (e.g. trip is too far in future), use fallback
        if not daily_weather:
            return get_historical_climate(lat, lon, start_date, end_date)

        avg_temp_max = round(sum(temps) / len(temps), 1) if temps else 20.0

        return {
            "daily": daily_weather,
            "avg_temp_max": avg_temp_max,
            "max_pop": max_pop,
            "is_cold": avg_temp_max < TEMP_COLD,
            "is_rainy": max_pop > RAIN_THRESHOLD
        }

    except Exception as e:
        print(f"Weather Fetch Error: {e}")
        return get_historical_climate(lat, lon, start_date, end_date)