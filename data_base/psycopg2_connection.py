from const import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB
from sqlalchemy import create_engine


DATABASE = (
    f'postgresql+psycopg2://{POSTGRES_USER}:'
    f'{POSTGRES_PASSWORD}@localhost/{POSTGRES_DB}'
)
ENGINE = create_engine(DATABASE, echo=True)
