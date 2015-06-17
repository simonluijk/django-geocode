import math
from geopy.distance import vincenty
from django.contrib.gis.geos import MultiPoint


def percentile(data_list, value):
    data_list = list(map(float, data_list))
    count = float(len(data_list))
    strict = len([i for i in data_list if i < value]) / count * 100
    weak = len([i for i in data_list if i <= value]) / count * 100
    return mean([strict, weak])


def mean(data_list):
    data_list = list(map(float, data_list))
    return sum(data_list) / len(data_list)


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


def calculate_center(points):
    center, distances = mean_distances(points)

    center_points = []
    center_distences = []
    for point, distance in zip(points, distances):
        if percentile(distances, distance) <= 80:
            center_points.append(point)
            center_distences.append(distance)

    if len(center_points):
        if mean(center_distences) <= 10:
            return mean_center(center_points)
        else:
            return calculate_center(center_points)
    else:
        return center
