import json
import os
from .utils import get_coordinates, find_nearest_bus_stop, find_route

def get_route_summary(origin, destination):
    associated_routes = []
    messages = []
    is_ori_stop , is_dest_stop, has_route = False, False, True
    true_destination = destination
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
                    destination = nearest_stop['name']
                else:
                    messages.append(f"Sorry, I could not find any nearest bus stop from {destination.capitalize()}.")
                    has_route = False
                    return "\n".join(messages)
            else:
                messages.append(f"Sorry, I could not find coordinates for {destination.capitalize()}.")
                has_route = False
                return "\n".join(messages)

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
                    messages.append(f"The nearest bus stop to {origin.capitalize()} is {nearest_stop['name']}")
                    origin = nearest_stop['name']
                else:
                    messages.append(f"Sorry, I could not find any nearest bus stop from {origin.capitalize()}.")
                    has_route = False
            else:
                messages.append(f"Sorry, I could not find coordinates for {origin.capitalize()}.")
                has_route = False

        # get route
        if has_route:
            final_routes = find_route(origin, destination, routes)
            messages.append(f"From {origin.capitalize()}, you can catch a bus to {destination.capitalize()} that follows the route:")
            for route in final_routes:
                messages.append(f"{route['route_name']}")
            if true_destination.lower() != destination.lower():
                messages.append(f"Then, you can go to {true_destination.capitalize()} from {destination.capitalize()}.")
        
    return "\n".join(messages) 

