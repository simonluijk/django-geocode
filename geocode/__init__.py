__version__ = '0.1.4'
VERSION = __version__

from .helpers import geocode_address, add_coordinates, delete_coordinates  # NOQA
from .signals import geocode_update  # NOQA
