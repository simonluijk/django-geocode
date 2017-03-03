from django.core.urlresolvers import reverse
from django.utils.html import mark_safe


def geocode_address(point_uuid, address, cluster=None, countdown=0):
    """
    Geo-codes an address. The result is returned in a signal.

    point_uuid: Unique identifier for the address in the system.
    cluster: A logical bucket to put the address in. This allows listeners to
        the signal to identify messages they are interested in.
    address: Address to be GEO coded.
    """
    from geocode.models import GeoAddress

    defaults = {'address': address, 'cluster': cluster}
    address, created = GeoAddress.objects.get_or_create(uuid=point_uuid,
                                                        defaults=defaults)
    address.run_geocode(countdown)
    return address


def add_coordinates(point_uuid, coordinates, tags=None, weight=None):
    """
    Adds coordinates to an address. A signal will be generated with updated
    coordinates.

    point_uuid: Unique identifier for the address in the system.
    coordinates: Coordinates to be added to the address data.
    """
    from geocode.models import GeoAddress

    address = GeoAddress.objects.get(uuid=point_uuid)
    address.add_coordinate(coordinates, tags, weight)
    address.send_geocode_update()
    return address


def delete_coordinates(point_uuid, tags=None, geocoders=False):
    """
    Delete coordinates from an address. A signal will be generated with updated
    coordinates.

    point_uuid: Unique identifier for the address in the system.
    tag: Only delete coordinates with this tag.
    """
    from geocode.models import GeoAddress

    address = GeoAddress.objects.get(uuid=point_uuid)
    address.delete_coordinate(tags=tags, geocoders=geocoders)
    address.send_geocode_update()
    return address


class GeocodeAdmin(object):

    def geocode_data(self, obj):
        """
        Allows adding link to geocode data from an objects admin change view.
        """
        from geocode.models import GeoAddress

        geocode = GeoAddress.objects.get(uuid=obj.point_uuid)
        url = reverse('admin:geocode_geoaddress_change', args=[geocode.id])
        return mark_safe('<a href="{0}">{1}</a>'.format(url, obj.point_uuid))
