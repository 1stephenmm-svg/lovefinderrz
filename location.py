import random
import requests

URL = "https://nominatim.openstreetmap.org/search"
HEADERS = {"User-Agent": "Lovefinderrz/1.0(1stephenmm@gmail.com)"}
DEFAULT_COORDINATES = {
    "Pasto": (1.2188, -77.2903),
    "Bogotá D.C.": (4.7149, -74.1788),
    "Cali": (3.5082, -76.6353),
    "Tumaco": (1.6754, -78.5979),
    "Túquerres": (1.1149, -77.6379),
    "Ipiales": (0.5899, -77.3747),
    "Tulcán": (0.6498, -78.3867),
    "Quito": (-0.0913, -78.6504),
}


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
