from celery import Celery
from slugify import slugify
from settings import MEDIA_DIR
from fastapi import UploadFile
from const import REDIS_HOST, REDIS_PORT
from data_base.psycopg2_connection import ENGINE
from data_base.models import Anime
from sqlalchemy.orm import sessionmaker
import os

REDIS_HOST = 'localhost'
worker = Celery(
    'worker',
    broker=f'redis://{REDIS_HOST}:{REDIS_PORT}',
    backend=f'redis://{REDIS_HOST}:{REDIS_PORT}/1'
)
worker.autodiscover_tasks()
worker.conf.event_serializer = 'pickle'
worker.conf.task_serializer = 'pickle'
worker.conf.result_serializer = 'pickle'
worker.conf.accept_content = [
    'application/json', 'application/x-python-serialize'
]
worker.conf.task_ignore_result = False
worker.conf.broker_connection_retry_on_startup = True
worker.conf.task_track_started = True


@worker.task
def save_video_task(anime_title, anime_id, filename, trailer):
    slug_title = slugify(anime_title)
    filename = f'trailer{os.path.splitext(filename)[-1]}'
    title_dir = os.path.join(MEDIA_DIR, slug_title)
    path = os.path.join(title_dir, filename)
    os.makedirs(title_dir, exist_ok=True)
    with open(path, 'wb') as f:
        f.write(trailer)
    with sessionmaker(ENGINE)() as session:
        anime = session.get(Anime, anime_id)
        anime.trailer = path
        session.commit()


def save_video_util(anime_title: str, anime_id: int, filename: str, trailer: UploadFile):
    trailer = trailer.file.read()
    save_video_task.apply_async(args=(anime_title, anime_id, filename, trailer))
