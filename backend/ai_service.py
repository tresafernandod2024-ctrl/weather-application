def get_weather_advice(temp, humidity, wind):

    advice = []

    if temp > 35:
        advice.append(
            "Wear light cotton clothes."
        )

        advice.append(
            "Stay hydrated throughout the day."
        )

    elif temp < 20:
        advice.append(
            "Carry a jacket."
        )

    else:
        advice.append(
            "Comfortable weather for outdoor activities."
        )

    if humidity > 80:
        advice.append(
            "Expect humid conditions."
        )

    if wind > 20:
        advice.append(
            "Be careful while travelling."
        )

    return " ".join(advice)