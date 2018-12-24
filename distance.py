# Name: Muhammad Mohsin Zafar
# Roll No. MS-18-ST-504826

# Distance Calculation using Haversine's Distance Formula
# https://en.wikipedia.org/wiki/Haversine_formula

import math


def get_distance_kms(lat_a, lon_a, lat_b, lon_b):
    earth_radius = 6371  # in km

    # Phi is Latitude value in Radians
    phi_1 = math.radians(lat_a)
    phi_2 = math.radians(lat_b)

    # Delta Phi is difference between Latitudes in Radians
    delta_phi = math.radians(lat_b - lat_a)

    # Delta Lambda is difference between Longitudes in Radians
    delta_lambda = math.radians(lon_b - lon_a)

    # Formula: a = sin^2(delta_phi/2) + cos(phi_!) * cos(phi_2) * sin^2(delta_lambda/2)
    a = (math.sin(delta_phi / 2) * math.sin(delta_phi / 2)) + \
        (math.cos(phi_1) * math.cos(phi_2) * math.sin(delta_lambda / 2) * math.sin(delta_lambda / 2))

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = earth_radius * c

    return d


# Test Code
if __name__ == '__main__':
    latitudeA = float(input("Enter value for City A's Latitude : "))
    longitudeA = float(input("Enter value for City A's Longitude : "))
    latitudeB = float(input("Enter value for City B's Latitude : "))
    longitudeB = float(input("Enter value for City B's Longitude : "))

    distance_in_km = get_distance_kms(latitudeA, longitudeA, latitudeB, longitudeB)
    print("Distance between City A and City B = ", distance_in_km)
