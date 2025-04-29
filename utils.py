from geopy.distance import geodesic
import requests

def get_coordinates(place_name):
    url = (
    f"https://nominatim.openstreetmap.org/search?"
    f"format=json&q={place_name}"
    f"&viewbox=85.25,27.75,85.45,27.65&bounded=1"
    )
    response = requests.get(url, headers={"User-Agent": "your-app-name-here"})
    data = response.json()
    if data:
        lat = float(data[0]['lat'])
        lon = float(data[0]['lon'])
        return (lat, lon)
    else:
        return None

def find_nearest_bus_stop(lat, lon, routes):
    nearest_stop = None
    min_distance = float('inf')

    for route in routes:
        for stop in route['stops']:
            stop_coords = (stop["lat"], stop["lon"])
            distance = geodesic((lat, lon), stop_coords).meters
            if distance < min_distance:
                min_distance = distance
                nearest_stop = stop

    return nearest_stop

def find_route(origin, destination, routes):
    matching_routes = []

    for route in routes:
        stops = [stop["name"].lower() for stop in route["stops"]]

        if origin.lower() in stops and destination.lower() in stops:
            matching_routes.append(route)

    return matching_routes