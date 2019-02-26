clean:
	docker-compose kill && docker-compose rm --force

build:
	docker-compose build progimage

run:
	docker-compose up -d progimage

run-prod:
	docker-compose up -d progimage-prod nginx

restart:
	docker-compose rm -sf progimage
	make run

exec:
	docker-compose exec progimage bash

test:
	docker-compose exec progimage python manage.py test

migrate:
	python manage.py migrate

ultimate: clean build run
	docker-compose exec progimage make migrate

ultimate-prod: clean build run-prod
	docker-compose exec progimage-prod make migrate
