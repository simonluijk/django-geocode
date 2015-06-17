from django.conf import settings

MIN_GEOCODES = getattr(settings, 'GEOCODE_MIN_GEOCODES', 2)
DATAPOINTS = getattr(settings, 'GEOCODE_DATAPOINTS', 50)

GEOCODERS = getattr(settings, 'GEOCODERS', (
    # Good open GeoCoders
    ('geopy.geocoders.GeocodeFarm', {}),
    ('geopy.geocoders.GoogleV3', {}),

    # Un-reliable open GeoCoders
    # ('geopy.geocoders.ArcGIS', {}),
    # ('geopy.geocoders.DataBC', {}),
    # ('geopy.geocoders.GeocoderDotUS', {}),
    # ('geopy.geocoders.NaviData', {}),
    # ('geopy.geocoders.Nominatim', {}),
    # ('geopy.geocoders.OpenMapQuest', {}),
    # ('geopy.geocoders.Yandex', {}),

    # Closed GeoCoders
    # ('geopy.geocoders.Baidu', {'api_key': ''}),
    # ('geopy.geocoders.Bing', {'api_key': ''}),
    # ('geopy.geocoders.GeoNames', {'username': ''}),
    # ('geopy.geocoders.IGNFrance', {'api_key': '',
    #                                'username': '',
    #                                'password': ''}),
    # ('geopy.geocoders.LiveAddress', {'auth_id': '', 'auth_token': ''}),
    # ('geopy.geocoders.OpenCage', {'api_key': ''}),
    # ('geopy.geocoders.YahooPlaceFinder', {'consumer_key': '',
    #                                       'consumer_secret': ''}),
    # ('geopy.geocoders.What3Words', {'api_key': ''}),
))
