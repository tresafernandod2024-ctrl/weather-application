from flask import Flask
from flask import request
from weather_service import get_weather_data

app = Flask(__name__)

@app.route("/weather")
def weather():

    city = request.args.get("city")

    if not city:
        return {
            "error": "City Required"
        }

    data = get_weather_data(city)

    return data

if __name__ == "__main__":
    app.run(debug=True)