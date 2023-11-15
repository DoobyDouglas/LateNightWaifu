from const import (
    REDIS_HOST,
    REDIS_PORT,
    POSTGRES_DB,
    POSTGRES_PASSWORD,
    POSTGRES_USER,
    DB_HOST,
)
from pathlib import Path

_BASE_DIR = Path.cwd()

MEDIA_DIR = 'media'

API_PREFIX = '/api'

# для разарботки
# REDIS_HOST = 'localhost'
REDIS_BROKER = f'redis://{REDIS_HOST}:{REDIS_PORT}'
REDIS_BACKEND = f'redis://{REDIS_HOST}:{REDIS_PORT}/1'
# для разарботки
# DB_HOST = 'localhost'
POSTGRES_URL = f'{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}/{POSTGRES_DB}'

VALID_IMAGE_EXT = ['image/jpeg', 'image/png']
# на прод
# 0.06
MAX_UPLOAD_IMAGE_SIZE = 1
# на прод
# 6
MAX_UPLOAD_VIDEO_SIZE = 25
