import requests


def get_weather_data(city):

    geo_response = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={
            "name": city,
            "count": 1
        }
    )

    geo_data = geo_response.json()

    if "results" not in geo_data:
        return {
            "error": "City not found"
        }

    latitude = geo_data["results"][0]["latitude"]
    longitude = geo_data["results"][0]["longitude"]

    response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": [
                "temperature_2m",
                "relative_humidity_2m",
                "wind_speed_10m",
                "weather_code"
            ],
            "daily": [
                "temperature_2m_max",
                "temperature_2m_min"
            ],
            "forecast_days": 7
        }
    )

    return response.json()