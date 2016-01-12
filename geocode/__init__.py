__version__ = '0.0.3'
VERSION = __version__

from .helpers import geocode_address, add_coordinates, delete_coordinates  # NOQA
from .signals import geocode_update  # NOQA
