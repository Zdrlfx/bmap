import json
import os
from .utils import get_coordinates, find_nearest_bus_stop, find_route

def get_route_summary(origin, destination):
    associated_routes = []
    messages = []
    is_ori_stop , is_dest_stop = False, False
    messages.append(f"{origin}->{destination}")
    # check if destination is a bus stop and set destination to bus stop rasa_bot\actions\backend\routes.json
    current_dir = os.path.dirname(os.path.abspath(__file__))
    routes_file_path = os.path.join(current_dir, "routes.json")
    with open(routes_file_path, 'r', encoding='utf-8') as f:
        routes = json.load(f)
        for route in routes:
            for stop in route['stops']:
                if stop['name'].lower() == destination.lower():
                    destination = stop['name']  # Get exact casing
                    is_dest_stop = True
                    break
            if is_dest_stop:
                break

        if not is_dest_stop:
            # get coordinates of destination
            coords = get_coordinates(destination)
            if coords:
                nearest_stop = find_nearest_bus_stop(coords[0], coords[1], routes)
                if nearest_stop:
                    messages.append(f"✅ Nearest bus stop to {destination} is {nearest_stop['name']}")
                    destination = nearest_stop['name']
                else:
                    messages.append("❌ Could not find nearest bus stop from destination.")
            else:
                messages.append("❌ Could not find coordinates for the destination.")

        # find routes containing destination 
        for route in routes:
            for stop in route['stops']:
                if stop['name'].lower() == destination.lower():
                    associated_routes.append(route)
                    break
            
        # check if origin is in routes of destination
        for route in associated_routes:
            for stop in route['stops']:
                if stop['name'].lower() == origin.lower(): 
                    is_ori_stop = True
                    break

        # if not find nearest stop from routes of destination
        if not is_ori_stop:
            # get coordinates of origin
            coords = get_coordinates(origin)
            if coords:
                nearest_stop = find_nearest_bus_stop(coords[0], coords[1], associated_routes)
                if nearest_stop:
                    messages.append(f"✅ Nearest bus stop to {origin} is {nearest_stop['name']}")
                    origin = nearest_stop['name']
                else:
                    messages.append("❌ Could not find nearest bus stop from origin.")
            else:
                messages.append("❌ Could not find coordinates for the origin.")

        # get route
        final_routes = find_route(origin, destination, routes)
        messages.append("Final Routes:")
        for route in final_routes:
            messages.append(f"Route Name: {route['route_name']}")
    
    return "\n".join(messages)

