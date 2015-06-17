from django import dispatch

geocode_update = dispatch.Signal(providing_args=['point_uuid', 'cluster',
                                                 'coordinates'])
