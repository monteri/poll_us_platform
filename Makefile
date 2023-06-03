build:
	docker-compose -f deploy/docker-compose.yml --project-directory . build

up:
	docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . up

shell:
	docker exec -it poll_us_platform-api-1 bash

prod-build:
	docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.prod.yml  --project-directory . build

prod-up:
	docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.prod.yml --project-directory . up

prod-background:
	docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.prod.yml --project-directory . up -d

stop:
	docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.prod.yml --project-directory . stop
