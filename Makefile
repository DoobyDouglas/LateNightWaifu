up:
	docker-compose up -d
run:
	docker start db
stop:
	docker stop db
migrations:
	alembic revision --autogenerate -m "migrations"
migrate:
	alembic upgrade head
app:
	python main.py
del:
	docker rm db
	docker volume rm latenightwaifu_database_alchemy