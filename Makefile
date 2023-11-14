up:
	docker-compose up -d
run:
	docker start db
	docker start redis
stop:
	docker stop db
	docker stop redis
	docker stop worker
	docker stop flower
migrations:
	alembic revision --autogenerate -m "migrations"
migrate:
	alembic upgrade head
app:
	python main.py
del:
	docker rm db
	docker rm redis
	docker volume rm latenightwaifu_database_volume
	docker volume rm latenightwaifu_redis_volume
reboot:
	docker stop db
	docker stop redis
	docker rm db
	docker rm redis
	docker volume rm latenightwaifu_database_volume
	docker volume rm latenightwaifu_redis_volume
	docker-compose up -d
work:
	celery -A worker.tasks:worker worker -l info --pool=solo
flow:
	celery -A worker.tasks:worker flower