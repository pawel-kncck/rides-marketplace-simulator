# in simulator/utils/helpers.py
import math

def calculate_distance(loc1: tuple, loc2: tuple) -> float:
    """Calculates the Euclidean distance between two locations."""
    return math.sqrt((loc1[0] - loc2[0])**2 + (loc1[1] - loc2[1])**2)
