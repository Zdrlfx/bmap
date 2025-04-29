from geopy.distance import geodesic
import requests
import json

# Load bus stop data
with open('latlong.json', 'r', encoding='utf-8') as f:
    bus_stops = json.load(f)

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

def find_nearest_bus_stop(lat, lon):
    nearest_stop = None
    min_distance = float('inf')

    for stop in bus_stops:
        stop_coords = (stop["lat"], stop["lon"])
        distance = geodesic((lat, lon), stop_coords).meters
        if distance < min_distance:
            min_distance = distance
            nearest_stop = stop

    return nearest_stop

# Example usage
place = input("Enter location: ")
coords = get_coordinates(place)

if coords:
    nearest = find_nearest_bus_stop(coords[0], coords[1])
    if nearest:
        print(f"✅ Nearest bus stop to {place} is {nearest['name']}")
else:
    print("❌ Could not find coordinates for the place.")
