import math
import pandas as pd
import argparse

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

def dms_to_decimal(dms):
    """
    Converts a DMS (degrees, minutes, seconds) string to decimal degrees.
    Example: '27 29 44.09 S' -> -27.49558
    """
    try:
        parts = dms.strip().split()
        degrees = float(parts[0])
        minutes = float(parts[1])
        seconds = float(parts[2])
        direction = parts[3]
        decimal = degrees + (minutes / 60) + (seconds / 3600)
        if direction in ['S', 'W']:
            decimal = -decimal
        return decimal
    except Exception as e:
        print(f"Error converting DMS to decimal: {e}")
        return None

def parse_csv(file_path):
    """
    Parses the CSV file and extracts latitude and longitude columns.
    Handles DMS and decimal degrees formats.
    """
    try:
        # Read the CSV file
        data = pd.read_csv(file_path)

        print("\nAvailable columns in the dataset:")
        print(data.columns)

        # Let the user choose columns for latitude and longitude
        lat_column = input("\nEnter the column name for Latitude (e.g., 'Latitude' or 'GPS Lat'): ").strip()
        lon_column = input("Enter the column name for Longitude (e.g., 'Longitude' or 'GPS Long'): ").strip()

        if lat_column not in data.columns or lon_column not in data.columns:
            print("Invalid column names. Please ensure you entered correct column names.")
            return []

        coordinates = []

        for index, row in data.iterrows():
            lat = row[lat_column]
            lon = row[lon_column]

            # Convert DMS to decimal degrees if necessary
            if isinstance(lat, str) and isinstance(lon, str):
                lat = dms_to_decimal(lat)
                lon = dms_to_decimal(lon)

            # Validate and append
            if is_valid_coordinate((lat, lon)):
                coordinates.append((lat, lon))
            else:
                print(f"Skipping invalid row {index + 1}: ({lat}, {lon})")

        return coordinates

    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return []

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

def main():
    parser = argparse.ArgumentParser(description="Process CSV files for coordinates.")
    parser.add_argument("--csv1", help="Path to the first CSV file")
    parser.add_argument("--csv2", help="Path to the second CSV file")
    args = parser.parse_args()

    # If CSV file paths are provided as arguments
    if args.csv1 and args.csv2:
        file1 = args.csv1
        file2 = args.csv2

        array1 = parse_csv(file1)
        array2 = parse_csv(file2)

        if array1 and array2:
            matches = find_closest_points(array1, array2)
            print("\nClosest matches:")
            for match in matches:
                print(f"From Array 1: {match['point_from_array1']} -> Closest in Array 2: {match['nearest_point_in_array2']} "
                      f"with Distance: {match['distance_km']} km")
        else:
            print("Both arrays must contain at least one valid point.")

    # If no arguments are provided, fall back to interactive mode
    else:
        while True:
            print("\nDo you want to upload a CSV file for coordinates?")
            mode = input("Enter 'csv' to upload a CSV file or 'exit' to quit: ").strip().lower()

            if mode == 'csv':
                file1 = input("\nEnter the file path for the first array (.csv): ").strip()
                file2 = input("Enter the file path for the second array (.csv): ").strip()

                array1 = parse_csv(file1)
                array2 = parse_csv(file2)

                if array1 and array2:
                    matches = find_closest_points(array1, array2)
                    print("\nClosest matches:")
                    for match in matches:
                        print(f"From Array 1: {match['point_from_array1']} -> Closest in Array 2: {match['nearest_point_in_array2']} "
                              f"with Distance: {match['distance_km']} km")
                else:
                    print("Both arrays must contain at least one valid point.")
            elif mode == 'exit':
                print("Exiting the program. Goodbye!")
                break
            else:
                print("Invalid input. Please enter 'csv' or 'exit'.")

if __name__ == "__main__":
    main()
