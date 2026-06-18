import requests

LYZR_API_URL = "https://agent-prod.studio.lyzr.ai/v3/inference/chat/"

API_KEY = "sk-default-9qtOTUzkSsZfPlCWqVPSK0MFHl8RQRtZ"

AGENT_ID = "6a342f247034b14329048f6c"

SESSION_ID = "weatherwise-session"
def get_ai_recommendation(weather_data):

    temperature = weather_data["current"]["temperature_2m"]
    humidity = weather_data["current"]["relative_humidity_2m"]
    wind = weather_data["current"]["wind_speed_10m"]

    prompt = f"""
Temperature: {temperature}°C
Humidity: {humidity}%
Wind Speed: {wind} km/h

Give:
1. Clothing suggestion
2. Activity recommendation
3. Health precaution

Maximum 80 words.
"""

    payload = {
        "user_id": "weatherwise_user",
        "agent_id": AGENT_ID,
        "session_id": SESSION_ID,
        "message": prompt
    }

    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    }

    response = requests.post(
        LYZR_API_URL,
        json=payload,
        headers=headers,
        timeout=30
    )

    data = response.json()

    return data.get(
        "response",
        "No recommendation available."
    )