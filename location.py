import random
import requests

from data import DEFAULT_COORDINATES
from math import radians, sin, cos, sqrt, atan2

URL = "https://nominatim.openstreetmap.org/search"
HEADERS = {"User-Agent": "Lovefinderrz/0.1.0 (1stephenmm@gmail.com)"}


def calculate_distance(origin, destination):
    """Calculate the distance in kilometers between two geographic coordinates.

    Uses the Haversine formula to calculate the great-circle distance
    between two points on Earth's surface.

    Args:
        origin (tuple): Latitude and longitude of the origin, in decimal
            degrees.
        destination (tuple): Latitude and longitude of the destination,
            in decimal degrees.

    Returns:
        float: Distance between the two coordinates in kilometers.

    Formula:
        Convert coordinates from degrees to radians:

            φ = latitude
            λ = longitude

        Calculate coordinate differences:

            Δφ = φ₂ - φ₁
            Δλ = λ₂ - λ₁

        Apply the Haversine formula:

            a = sin²(Δφ / 2) + cos(φ₁) · cos(φ₂) · sin²(Δλ / 2)

            c = 2 · atan2(√a, √(1 - a))

        Calculate the distance:

            d = R · c

        Where:
            R = 6371 km (Earth's mean radius)
            d = great-circle distance in kilometers
    """

    # Get latitudes and longitudes
    origin_lat, origin_lon = origin
    destination_lat, destination_lon = destination

    # Convert degrees to radians
    (
        origin_lat,
        origin_lon,
        destination_lat,
        destination_lon,
    ) = map(
        radians,
        [
            origin_lat,
            origin_lon,
            destination_lat,
            destination_lon,
        ],
    )

    # coordinates difference
    delta_lat = destination_lat - origin_lat
    delta_lon = destination_lon - origin_lon

    # Haversine formula
    a = (
        sin(delta_lat / 2) ** 2
        + cos(origin_lat) * cos(destination_lat) * sin(delta_lon / 2) ** 2
    )

    return 6371 * (2 * atan2(sqrt(a), sqrt(1 - a)))  # distance in kilometers


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
