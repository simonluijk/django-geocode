from django.test import TestCase
from geopy.distance import vincenty
from geopy.location import Location
from geopy.point import Point
from mock import patch, ANY


def compare(test_value, other, accuratcy):
    if not type(test_value) == type(other):
        return False

    # Coordinates are equal if within x meters.
    distance_meters = vincenty(test_value, other).m
    if distance_meters > accuratcy:
        msg = 'Distance {0} greater then {1} meters.'.format(
            distance_meters, accuratcy)
        raise AssertionError(msg)

    return True


class Matcher(object):
    def __init__(self, compare, test_value, accuratcy):
        self.compare = compare
        self.test_value = test_value
        self.accuratcy = accuratcy

    def __eq__(self, other):
        return self.compare(self.test_value, other, self.accuratcy)


class GeoCodeTestCase(TestCase):

    def get_patch(self, name):
        patcher = patch(name)
        thing = patcher.start()
        self.addCleanup(patcher.stop)
        return thing

    def setUp(self):
        self.geocoders = []
        good_geocoders = [
            'geopy.geocoders.GeocodeFarm.geocode',
        ]

        for geocoder in good_geocoders:
            geo = self.get_patch(geocoder)
            geo.return_value = Location(point=Point([48.8582653, 2.2944946]))
            self.geocoders.append(geo)

        bad_geocoders = [
            'geopy.geocoders.GoogleV3.geocode',
        ]

        for geocoder in bad_geocoders:
            geo = self.get_patch(geocoder)
            geo.return_value = Location(point=Point([48.8581653, 2.2944946]))
            self.geocoders.append(geo)

    @patch('geocode.geocode_update.send')
    def test_initial_geocode(self, geocode_update):
        """
        Test GEO coding of initial address.
        """
        from geocode import geocode_address
        from uuid import uuid4

        point_uuid = uuid4()
        geocode_address(point_uuid, 'Eiffel Tower, Paris, France')

        match_coordinates = Matcher(compare, [48.8582653, 2.2944946], 6)
        geocode_update.assert_called_once_with(sender=ANY,
                                               cluster=None,
                                               point_uuid=point_uuid,
                                               coordinates=match_coordinates)

        self.assertEqual(len(self.geocoders), 2)
        for geocoder in self.geocoders:
            geocoder.assert_called_once_with('Eiffel Tower, Paris, France')

    @patch('geocode.geocode_update.send')
    def test_add_coordinates(self, geocode_update):
        """
        Test adding extra details.
        """
        from geocode import geocode_address, add_coordinates
        from uuid import uuid4

        point_uuid = uuid4()
        geocode_address(point_uuid, 'Eiffel Tower, Paris, France',
                        cluster='test')
        geocode_update.reset_mock()

        add_coordinates(point_uuid, [48.8582653, 2.2944946], tags=['ios', ])

        match_coordinates = Matcher(compare, [48.8582653, 2.2944946], 4)
        geocode_update.assert_called_once_with(sender=ANY,
                                               cluster='test',
                                               point_uuid=point_uuid,
                                               coordinates=match_coordinates)

    @patch('geocode.geocode_update.send')
    def test_regression_disparate_coordinates(self, geocode_update):
        """
        Regression test for when a mean center can not be found. This happens
        if all coordinates are far apart.
        """
        from geocode.models import GeoAddress
        from uuid import uuid4

        point_uuid = uuid4()
        address = GeoAddress.objects.create(uuid=point_uuid, cluster='reg')
        address.add_coordinate([48.8582653, 2.2944946], ['ios', ])
        address.add_coordinate([48.8582653, 1.2944946], ['ios', ])
        address.add_coordinate([48.8582653, 0.2944946], ['ios', ])
        address.send_geocode_update()

        match_coordinates = Matcher(compare, [48.8582653, 1.2944946], 3)
        geocode_update.assert_called_once_with(sender=ANY,
                                               cluster='reg',
                                               point_uuid=point_uuid,
                                               coordinates=match_coordinates)
