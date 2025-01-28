import math

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculates the distance in kilometers between two points on Earth 
    by longitude and latitude using the Haversine formula.
    """
    earth_radius = 6371.0  # Earth radius in kilometers
    
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Getting difference between the two points
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return earth_radius * c

def dms_to_decimal(degrees, minutes=0, seconds=0):
    """
    Converts degrees, minutes, and seconds (DMS) to decimal degrees.
    """
    decimal = abs(degrees) + minutes / 60 + seconds / 3600
    return -decimal if degrees < 0 else decimal

def parse_coordinate(entry):
    """
    Parses a coordinate string in either decimal degrees or DMS format.
    Args:
    - entry: A string representing a coordinate.
    
    Returns:
    - A tuple (latitude, longitude) in decimal degrees, or None if invalid.
    """
    try:
        entry = entry.strip()
        if "," not in entry:
            raise ValueError("Invalid format: No comma found in input.")

        lat, lon = entry.split(",")

        # Handle DMS input (e.g., "40°44'55", -73°59'11")
        def parse_single(coord):
            if "°" in coord:
                parts = coord.replace("°", " ").replace("'", " ").replace('"', "").split()
                degrees, minutes, seconds = map(float, parts + [0] * (3 - len(parts)))  # Fill missing values with 0
                return dms_to_decimal(degrees, minutes, seconds)
            else:
                # Assume it's in decimal degrees
                return float(coord)

        lat = parse_single(lat)
        lon = parse_single(lon)

        if is_valid_coordinate((lat, lon)):
            return (lat, lon)
        else:
            print(f"Invalid coordinate range: ({lat}, {lon}). Latitude must be between -90 and 90, and longitude between -180 and 180.")
            return None
    except Exception as e:
        print(f"Invalid input: '{entry}'. Please enter coordinates in decimal degrees (e.g., '40.748817,-73.985428') or DMS (e.g., '40°44'55, -73°59'11').")
        return None

def is_valid_coordinate(coord):
    """
    Validates if the given coordinate is a valid latitude and longitude on Earth.
    Args:
    - coord: A tuple of (latitude, longitude) to validate.
    
    Returns:
    - True if valid, False otherwise.
    """
    if not isinstance(coord, tuple) or len(coord) != 2:
        return False
    lat, lon = coord
    return -90 <= lat <= 90 and -180 <= lon <= 180

def get_coordinates_input(prompt):
    """
    Gets a list of coordinates from the user.
    Args:
    - prompt: Instruction for the user.
    
    Returns:
    - List of tuples with valid latitude and longitude.
    """
    print(prompt)
    coordinates = []
    while True:
        entry = input("Enter coordinates as 'latitude,longitude' (decimal degrees or DMS) or press Enter to finish: ")
        if not entry:
            break
        coord = parse_coordinate(entry)
        if coord in coordinates:
            print("Duplicate coordinate added, input not added.")
        if coord:
            coordinates.append(coord)
    return coordinates

def find_closest_points(array1, array2):
    """
    Match each point in the first array to the closest point in the second array.
    Args:
    - array1: List of tuples representing (latitude, longitude)
    - array2: List of tuples representing (latitude, longitude)
    
    Returns:
    - List of dictionaries containing the matched points and distances
    """
    nearest_neighbors = []
    
    for i, (lat1, lon1) in enumerate(array1):
        min_distance = float('inf')
        nearest_point = None
        for lat2, lon2 in array2:
            distance = haversine(lat1, lon1, lat2, lon2)
            if distance < min_distance:
                min_distance = distance
                nearest_point = (lat2, lon2)
        nearest_neighbors.append({
            "point_from_array1": (lat1, lon1),
            "nearest_point_in_array2": nearest_point,
            "distance_km": round(min_distance, 2)
        })
    
    return nearest_neighbors

# Main program loop
while True:
    print("\nEnter points for the first array:")
    array1 = get_coordinates_input("Input points for Array 1 (e.g., 40.748817,-73.985428 or 40°44'55, -73°59'11):")

    print("\nEnter points for the second array:")
    array2 = get_coordinates_input("Input points for Array 2 (e.g., 37.774929,-122.419416 or 37°46'30, -122°25'10):")

    if array1 and array2:
        matches = find_closest_points(array1, array2)
        print("\nClosest matches:")
        for match in matches:
            print(f"From Array 1: {match['point_from_array1']} -> Closest in Array 2: {match['nearest_point_in_array2']} "
                  f"with Distance: {match['distance_km']} km")
    else:
        print("Both arrays must contain at least one valid point.")
            
    while True:
        # Ask the user if they want to process another pair of arrays
        again = input("\nDo you want to process another pair of arrays? (yes/no): ").strip().lower()
        
        if again == 'no':
            print("Exiting the program. Goodbye!")
            exit()
        elif again == 'yes':
            break
        else:
            print("Invalid input, please input one of the options: yes/no.")