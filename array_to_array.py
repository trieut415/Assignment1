import math

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculates the distance in kilometers between two points on Earth 
    by longitude and latitude using the Haversine formula.
    """
    # Earth radius in kilometers
    earth_radius = 6371.0  
    
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Getting difference between the two points
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    # Haversine formula (taken from chatgpt)
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return earth_radius * c

def find_closest_points(array1, array2):
    """
    Match each point in the first array to the closest point in the second array.
    Args:
    - array1: List of tuples representing (latitude, longitude)
    - array2: List of tuples representing (latitude, longitude)
    
    Returns:
    - List of tuples: Each tuple contains an index from array1 and the index of the nearest point in array2
    """
    nearest_neighbor = []
    
    for i, (lat1, lon1) in enumerate(array1):
        min_distance = float('inf')
        nearest_index = -1
        for j, (lat2, lon2) in enumerate(array2):
            distance = haversine(lat1, lon1, lat2, lon2)
            if distance < min_distance:
                min_distance = distance
                nearest_index = j
        nearest_neighbor.append((i, nearest_index))
    
    return nearest_neighbor

# Example usage (generated from chatgpt)
array1 = [(40.748817, -73.985428), (34.052235, -118.243683), (51.507222, -0.1275)]  # NYC, LA, London
array2 = [(37.774929, -122.419416), (48.856613, 2.352222), (40.73061, -73.935242)]  # SF, Paris, Brooklyn

matches = find_closest_points(array1, array2)
print("Closest matches (index mapping):", matches)
