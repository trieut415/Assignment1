import pytest
from array_to_array import haversine, dms_to_decimal, is_valid_coordinate, find_closest_points

def test_haversine():
    # Test distance between two points
    assert round(haversine(0, 0, 0, 90), 2) == 10007.54  # Quarter of Earth's circumference
    assert haversine(0, 0, 0, 0) == 0  # Same point

@pytest.mark.parametrize("lat1, lon1, lat2, lon2, expected", [
    (0, 0, 0, 0, 0),                # Same point
    (0, 0, 0, 180, 20015.09),      # Half of Earth's circumference
    (0, 0, 90, 0, 10007.54),       # Quarter of Earth's circumference
])
def test_haversine_parametrized(lat1, lon1, lat2, lon2, expected):
    assert round(haversine(lat1, lon1, lat2, lon2), 2) == expected

def test_dms_to_decimal():
    # Test DMS to decimal conversion
    assert dms_to_decimal("27 29 44.09 S") == pytest.approx(-27.49558, rel=1e-5)
    assert dms_to_decimal("85 32 45.12 N") == pytest.approx(85.5458667, rel=1e-5)
    assert dms_to_decimal("invalid input") is None  # Test error handling

def test_is_valid_coordinate():
    # Test valid and invalid coordinates
    assert is_valid_coordinate((90, 180)) is True
    assert is_valid_coordinate((-90, -180)) is True
    assert is_valid_coordinate((91, 0)) is False  # Invalid latitude
    assert is_valid_coordinate((0, 181)) is False  # Invalid longitude
    assert is_valid_coordinate("invalid") is False

def test_find_closest_points():
    # Test finding closest points
    array1 = [(0, 0), (10, 10)]
    array2 = [(0, 90), (15, 15), (-10, -10)]
    results = find_closest_points(array1, array2)
    
    # Correct expected results based on distance calculations
    assert results[0]["nearest_point_in_array2"] == (-10, -10)  # Closest to (0, 0)
    assert results[1]["nearest_point_in_array2"] == (15, 15)   # Closest to (10, 10)
    assert results[0]["distance_km"] == pytest.approx(1568.52, rel=1e-2)
    assert results[1]["distance_km"] == pytest.approx(776.86, rel=1e-2)
