from flask import Flask
from flask import request

from weather_service import get_weather_data
from lyzr_service import get_ai_recommendation

app = Flask(__name__)


@app.route("/weather")
def weather():

    city = request.args.get("city")

    if not city:
        return {
            "error": "City Required"
        }

    weather_data = get_weather_data(city)

    try:

        recommendation = get_ai_recommendation(
            weather_data
        )

        weather_data["ai_recommendation"] = recommendation

    except Exception:

        weather_data["ai_recommendation"] = (
            "AI recommendation unavailable."
        )

    return weather_data


if __name__ == "__main__":
    app.run(debug=True)