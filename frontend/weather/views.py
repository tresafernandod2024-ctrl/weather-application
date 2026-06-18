from django.shortcuts import render
from django.http import JsonResponse
import requests

FLASK_API = "http://127.0.0.1:5000/weather"


def home(request):

    context = {}

    if request.method == "POST":

        city = request.POST.get("city", "").strip()

        if not city:

            return render(
                request,
                "index.html",
                {
                    "error": "Please enter a city name."
                }
            )

        try:

            geo_response = requests.get(
                "https://geocoding-api.open-meteo.com/v1/search",
                params={
                    "name": city,
                    "count": 1
                },
                timeout=5
            )

            geo = geo_response.json()

            if "results" not in geo:

                return render(
                    request,
                    "index.html",
                    {
                        "error": "City not found."
                    }
                )

            city_name = geo["results"][0]["name"]
            state = geo["results"][0].get("admin1", "")
            country = geo["results"][0].get("country", "")

            full_city = f"{city_name}, {state}, {country}"

            flask_response = requests.get(
                FLASK_API,
                params={
                    "city": city_name
                },
                timeout=10
            )

            if flask_response.status_code != 200:

                return render(
                    request,
                    "index.html",
                    {
                        "error": "Weather API returned an error."
                    }
                )

            weather = flask_response.json()

            context = {
                "city": full_city,
                "weather": weather,
                "recommendation": weather.get(
                    "ai_recommendation",
                    "No recommendation available."
                )
            }

        except requests.exceptions.ConnectionError:

            return render(
                request,
                "index.html",
                {
                    "error": "Backend Flask server is not running."
                }
            )

        except requests.exceptions.Timeout:

            return render(
                request,
                "index.html",
                {
                    "error": "Weather service timed out."
                }
            )

        except Exception as e:

            return render(
                request,
                "index.html",
                {
                    "error": str(e)
                }
            )

    return render(
        request,
        "index.html",
        context
    )


def autocomplete(request):

    query = request.GET.get("query", "").strip()

    if len(query) < 2:
        return JsonResponse([], safe=False)

    try:

        response = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={
                "name": query,
                "count": 10,
                "language": "en"
            },
            timeout=5
        )

        data = response.json()

        cities = []

        if "results" in data:

            for item in data["results"]:

                city_name = item.get("name")

                country = item.get("country", "")

                if city_name:

                    cities.append(
                        f"{city_name}, {country}"
                    )

        return JsonResponse(cities, safe=False)

    except:

        return JsonResponse([], safe=False)