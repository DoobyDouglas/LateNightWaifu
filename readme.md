Необходимо задать путь к базе в alembic.ini и импортировать метадату в alembic/env.py
Команды для alembic:

alembic init alembic

alembic revision --autogenerate -m "some name"

alembic upgrade "revision_id"

alembic upgrade head


{
  "username": "dooby",
  "email": "dooby@mail.com",
  "password": "dooby"
}

{
  "username": "string",
  "email": "user@example.com",
  "password": "string"
}