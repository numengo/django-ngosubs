__version__ = '0.1.0'

from simple_settings import LazySettings
settings = LazySettings('ngosubs.config.settings', 'NGOSUBS_.environ')
from ngoschema.loaders import register_module

register_module('ngosubs')

__all__ = [
    'settings',
]
