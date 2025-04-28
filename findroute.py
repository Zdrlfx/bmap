#if both bus stops
# compare with bus stop list and give out route

import json

# Load the bus routes from the file
with open('bus.json', 'r', encoding='utf-8') as f:
    bus_routes = json.load(f)

def find_route(origin, destination):
    matching_routes = []

    for route in bus_routes:
        stops = [stop.lower() for stop in route["stops"]]

        if origin.lower() in stops and destination.lower() in stops:
            matching_routes.append(route)

    return matching_routes

# Example usage
origin = input("Enter origin stop: ")
destination = input("Enter destination stop: ")

routes = find_route(origin, destination)

if routes:
    for r in routes:
        print(f"✅ Found route: {r['route_name']}")
else:
    print("❌ Sorry, no route found from", origin, "to", destination)
