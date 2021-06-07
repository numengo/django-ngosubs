__version__ = '0.1.0'

from simple_settings import LazySettings
settings = LazySettings('ngosubs.config.settings', 'NGOSUBS_.environ')

__all__ = [
    'settings',
]
