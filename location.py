import random
import requests

from data import DEFAULT_COORDINATES

URL = "https://nominatim.openstreetmap.org/search"
HEADERS = {"User-Agent": "Lovefinderrz/1.0(1stephenmm@gmail.com)"}


def get_city_area(city):
    response = requests.get(
        url=URL,
        params={"q": city, "format": "json", "addressdetails": 0, "limit": 1},
        headers=HEADERS,
    )
    response.raise_for_status()
    data = response.json()

    if not data:
        raise ValueError("Ciudad no encontrada.")

    return data[0]["boundingbox"]


def generate_location(city_area):
    south, north, west, east = map(float, city_area)
    latitude = random.uniform(south, north)
    longitude = random.uniform(west, east)
    return latitude, longitude


def get_random_location(city):
    try:
        city_area = get_city_area(city)
        return generate_location(city_area)
    except requests.RequestException:
        coordinates = DEFAULT_COORDINATES.get(city)

        if coordinates is not None:
            return coordinates

        raise
