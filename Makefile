up:
	docker-compose up -d
run:
	docker start db
stop:
	docker stop db
migrations:
	alembic revision --autogenerate -m "migrations"