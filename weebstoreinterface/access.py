from os.path import dirname, abspath, join

# Default False
ACCESS_DEBUG = True

BASE_DIR = dirname(dirname(abspath(__file__)))

ACCESS_MEDIA_ROOT = join(BASE_DIR, 'media')
ACCESS_STATIC_ROOT = join(BASE_DIR, '.static')
