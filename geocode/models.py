from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.utils.translation import ugettext_lazy as _

try:
    from django.db.models import UUIDField
    # Django 1.8 now includes a UUIDField (database representation differs)
except ImportError:
    from uuidfield import UUIDField

from geocode import conf
from geocode.utils import calculate_center


class GeoAddress(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    uuid = UUIDField(unique=True)
    cluster = models.CharField(_('Cluster'), max_length=50, null=True)
    address = models.TextField()

    class Meta:
        verbose_name = _('Geo address')
        verbose_name_plural = _('Geo addresses')
        ordering = ('-created', )

    def __unicode__(self):
        return self.address

    @property
    def coordinates(self):
        """
        Return the estimated location based on the GEO-coding results.
        Currently we are simply ignoring anything with a distance from the mean
        center that is greater then the 80 percentile of all distances from the
        mean center. Falling back to the mean center if all point are outside
        the 80 percentile.
        """
        points = []
        for point in self.geodata_set.all()[:conf.DATAPOINTS]:
            for i in range(0, point.weight):
                points.append(point.point)
        center = calculate_center(points)
        return [center.x, center.y]

    def run_geocode(self):
        from geocode.tasks import geocode_address_task
        geocode_address_task.delay(self.uuid)

    def send_geocode_update(self):
        from geocode.signals import geocode_update
        geocode_update.send(sender=GeoAddress,
                            point_uuid=self.uuid,
                            cluster=self.cluster,
                            coordinates=self.coordinates)

    def add_coordinate(self, coordinates, tags=None, weight=None):
        if tags is None:
            tags = ['not-set', ]

        if weight is None:
            weight = 1

        tags = [tag.lower() for tag in tags]
        for tag in tags:
            Tag.objects.get_or_create(tag=tag)
        tags = ','.join(tags)

        self.geodata_set.create(point=Point(*coordinates), tags=tags,
                                weight=weight)

    def delete_coordinate(self, tag):
        self.geodata_set.filter(tags__icontains=tag).delete()


class GeoData(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    address = models.ForeignKey(GeoAddress)
    point = models.PointField(srid=4326)
    tags = models.CharField(max_length=255)
    weight = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = _('Geo data')
        verbose_name_plural = _('Geo data')
        ordering = ('-created', )

    def __unicode__(self):
        return '{0.x}, {0.y}'.format(self.point)


class Tag(models.Model):
    tag = models.CharField(_('Tag'), max_length=50, unique=True)

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

    def __unicode__(self):
        return self.tag
