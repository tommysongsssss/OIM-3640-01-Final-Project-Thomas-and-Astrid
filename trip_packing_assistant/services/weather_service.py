import requests
from datetime import datetime
from config import Config

def get_coordinates(city_name):
    """Fetches Lat/Lon for a city name."""
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={Config.OPENWEATHER_API_KEY}"
    resp = requests.get(url)
    if resp.status_code == 200 and resp.json():
        data = resp.json()[0]
        return data['lat'], data['lon']
    return None, None

def get_trip_weather(lat, lon, start_date, end_date):
    """
    Fetches 5-day/3-hour forecast and aggregates it into a simple trip summary.
    Note: Free tier keys often don't support the 'OneCall' daily API, 
    so we use the standard 'forecast' endpoint.
    """
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&appid={Config.OPENWEATHER_API_KEY}"
    resp = requests.get(url)
    data = resp.json()

    daily_summary = []
    max_temps = []
    rain_probs = []

    # Simple aggregation of the 3-hour blocks
    for item in data.get('list', []):
        dt = datetime.fromtimestamp(item['dt'])
        # Only include days within user's range (OpenWeather only gives 5 days ahead)
        if start_date.date() <= dt.date() <= end_date.date():
            max_temps.append(item['main']['temp_max'])
            rain_probs.append(item.get('pop', 0))
            
            # Grab a midday weather description for the list
            if dt.hour == 12:
                daily_summary.append({
                    'date': dt.strftime('%Y-%m-%d'),
                    'temp': item['main']['temp'],
                    'desc': item['weather'][0]['description'],
                    'pop': item.get('pop', 0)
                })

    # If dates are too far in future, return generic fallback
    if not max_temps:
        return {
            'days': [],
            'avg_temp_max': 20, # fallback
            'max_pop': 0.0,
            'is_cold': False,
            'is_rainy': False
        }

    overall_max_temp = max(max_temps)
    overall_rain_prob = max(rain_probs)

    from config import TEMP_COLD, RAIN_THRESHOLD
    return {
        'days': daily_summary,
        'avg_temp_max': round(sum(max_temps)/len(max_temps), 1),
        'max_pop': overall_rain_prob,
        'is_cold': overall_max_temp < TEMP_COLD,
        'is_rainy': overall_rain_prob > RAIN_THRESHOLD
    }