# input origin and destination
origin = input("Enter origin: ")
destination = input("Enter destination: ")

# check if destination is a bus stop and set destination to bus stop
with open(bus.json, 'r', encoding='utf-8') as f:
    bus_stops = json.load(f)
    for stop in bus_stops:
        if stop['name'].lower() == destination.lower():
            destination = stop['name']
            is_stop = True
            break

if not is_stop:
    # get coordinates of destination
    coords = get_coordinates(destination)
    if coords:
        nearest_stop = find_nearest_bus_stop(coords[0], coords[1])
        if nearest_stop:
            destination = nearest_stop['name']
            print(f"✅ Nearest bus stop to {destination} is {nearest_stop['name']}")
        else:
            print("❌ Could not find nearest bus stop.")
    else:
        print("❌ Could not find coordinates for the place.")

# find routes containing destination 

# check if origin is in routes of destination
# if not find nearest stop from routes of destination
# get route