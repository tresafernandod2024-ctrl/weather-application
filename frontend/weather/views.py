from django.shortcuts import render
from django.http import JsonResponse
import requests

FLASK_API = "http://127.0.0.1:5000/weather"


def home(request):

    context = {}

    if request.method == "POST":

        city = request.POST.get("city")

        geo = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={
                "name": city,
                "count": 1
            }
        ).json()

        if "results" not in geo:

            return render(
                request,
                "index.html",
                {
                    "error": "City not found"
                }
            )

        city_name = geo["results"][0]["name"]
        state = geo["results"][0].get("admin1", "")
        country = geo["results"][0].get("country", "")

        full_city = f"{city_name}, {state}, {country}"

        response = requests.get(
            FLASK_API,
            params={
                "city": city_name
            }
        )

        if response.status_code == 200:

            weather = response.json()

            context = {
                "city": full_city,
                "weather": weather
            }

    return render(
        request,
        "index.html",
        context
    )


def autocomplete(request):

    query = request.GET.get("query", "")

    if len(query) < 2:
        return JsonResponse([], safe=False)

    response = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={
            "name": query,
            "count": 10,
            "language": "en"
        }
    )

    data = response.json()

    cities = []

    if "results" in data:

        for item in data["results"]:

            feature = item.get("feature_code", "")

            if feature in [
                "PPLC",
                "PPLA",
                "PPLA2",
                "PPLA3",
                "PPLA4"
            ]:

                cities.append(
                    f"{item['name']}, {item.get('country','')}"
                )

    return JsonResponse(cities, safe=False)