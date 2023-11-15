up:
	docker-compose up -d
run:
	docker start db
	docker start redis
	docker start worker
	docker start flower
	docker start web
	docker start nginx
stop:
	docker stop db
	docker stop redis
	docker stop worker
	docker stop flower
	docker stop web
	docker stop nginx
migrations:
	alembic revision --autogenerate -m "migrations"
migrate:
	alembic upgrade head
app:
	python main.py
del:
	docker rm db
	docker rm redis
	docker rm worker
	docker rm flower
	docker rm web
	docker rm nginx
	docker volume rm latenightwaifu_database_volume
	docker volume rm latenightwaifu_redis_volume
reboot:
	docker stop db
	docker stop redis
	docker stop worker
	docker stop flower
	docker stop web
	docker stop nginx
	docker rm db
	docker rm redis
	docker rm worker
	docker rm flower
	docker rm web
	docker rm nginx
	docker volume rm latenightwaifu_database_volume
	docker volume rm latenightwaifu_redis_volume
	docker-compose up -d
work:
	celery -A worker.tasks:worker worker -l info --pool=solo
flow:
	celery -A worker.tasks:worker flower
build:
	docker-compose up -d --build