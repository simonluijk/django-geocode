from django.core.urlresolvers import reverse
from django.utils.html import mark_safe
from geocode.models import GeoAddress


def geocode_address(point_uuid, address, cluster=None):
    """
    Geo-codes an address. The result is returned in a signal.

    point_uuid: Unique identifier for the address in the system.
    cluster: A logical bucket to put the address in. This allows listeners to
        the signal to identify messages they are interested in.
    address: Address to be GEO coded.
    """
    address, created = GeoAddress.objects.get_or_create(uuid=point_uuid,
                                                        cluster=cluster,
                                                        address=address)
    address.run_geocode()


def add_coordinates(point_uuid, coordinates, tags=None):
    """
    Adds coordinates to an address. A signal will be generated with updated
    coordinates.

    point_uuid: Unique identifier for the address in the system.
    coordinates: Coordinates to be added to the address data.
    """
    address = GeoAddress.objects.get(uuid=point_uuid)
    address.add_coordinate(coordinates, tags)
    address.send_geocode_update()


class GeocodeAdmin(object):

    def geocode_data(self, obj):
        """
        Allows adding link to geocode data from an objects admin change view.
        """
        geocode = GeoAddress.objects.get(uuid=obj.point_uuid)
        url = reverse('admin:geocode_geoaddress_change', args=[geocode.id])
        return mark_safe('<a href="{0}">{1}</a>'.format(url, obj.point_uuid))
