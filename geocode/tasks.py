import logging

from geopy.exc import GeopyError
from celery import shared_task

from geocode import conf
from geocode.models import GeoAddress

try:
    # Django 1.7 and onwards.
    from django.utils.module_loading import import_string
except ImportError:
    # Older version of Django.
    from django.utils.module_loading import import_by_path as import_string


logger = logging.getLogger('geocode')


geocoders = []
for import_path, kwargs in conf.GEOCODERS:
    Geocoder = import_string(import_path)
    geocoders.append((Geocoder(**kwargs), import_path.split('.')[-1]))


@shared_task(bind=True, default_retry_delay=60*3, max_retries=20,
             ignore_result=True)
def geocode_address_task(self, pk):
    address = GeoAddress.objects.get(pk=pk)

    success_count = 0
    for geocoder, tag in geocoders:
        try:
            location = geocoder.geocode(address.address)
        except (GeopyError, IndexError) as e:
            logger.info(e)
        else:
            if location:
                coordinates = [location.latitude, location.longitude]
                address.add_coordinate(coordinates, tags=[tag, ])
                success_count += 1

    if success_count < min(conf.MIN_GEOCODES, len(geocoders)):
        self.retry()

    address.send_geocode_update()
