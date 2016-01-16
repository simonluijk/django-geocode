import math
from geopy.distance import vincenty
from django.contrib.gis.geos import Point, MultiPoint


def percentile(data_list, value):
    data_list = list(map(float, data_list))
    count = float(len(data_list))
    strict = len([i for i in data_list if i < value]) / count * 100
    weak = len([i for i in data_list if i <= value]) / count * 100
    return mean([strict, weak])


def mean(data_list):
    length = len(data_list)
    if length == 0:
        return 0
    data_list = list(map(float, data_list))
    return sum(data_list) / length


def mean_center(points):
    return MultiPoint(points).centroid


def standard_deviation(data_list):
    data_list = list(map(float, data_list))
    mean_value = mean(data_list)
    deviations = [i - mean_value for i in data_list]
    deviations_squared = [math.pow(i, 2) for i in deviations]
    mean_deviation = mean(deviations_squared)
    return math.sqrt(mean_deviation)


def mean_distances(points):
    mean = mean_center(points)
    return mean, [vincenty(p, mean).meters for p in points]


def calculate_center(points, depth=0):
    """
    Finds the mean center of the provided points. Returns when it finds a
    cluster of points who's mean distance from the mean center is less
    then 10 meters or when the max depth (20) is reached. On each iteration it
    removes the furthest 5 percentile from the center.
    """

    if len(points) == 0:
        return Point(0, 0)

    center, distances = mean_distances(points)
    if mean(distances) <= 10 or depth > 20:
        return center

    percentiles = [percentile(distances, d) for d in distances]
    max_percentile = max(percentiles) * 0.95

    center_points = []
    center_distences = []
    for i, point_percentile in enumerate(percentiles):
        if point_percentile <= max_percentile:
            center_points.append(points[i])
            center_distences.append(distances[i])

    if len(center_points):
        return calculate_center(center_points, depth=depth + 1)
    else:
        return center
