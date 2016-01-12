from django.contrib.gis import admin
from geocode.models import GeoAddress, GeoData


class GeoDataInline(admin.TabularInline):
    model = GeoData
    extra = 0
    fields = ('created', 'address', 'tags', 'point', 'weight')
    readonly_fields = ('created', 'address', 'tags', 'point', 'weight')

    def has_add_permission(self, *args):
        return False


class GeoAddressAdmin(admin.OSMGeoAdmin):
    inlines = [GeoDataInline, ]
    list_display = ('created', 'uuid', 'cluster', 'address')
    search_fields = ('address', )
    fields = ('created', 'uuid', 'cluster', 'address', 'coordinates')
    readonly_fields = ('created', 'uuid', 'cluster', 'address', 'coordinates')

    def has_add_permission(self, *args):
        return False

    def has_delete_permission(self, *args):
        return False

admin.site.register(GeoAddress, GeoAddressAdmin)
