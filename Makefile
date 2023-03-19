build:
	docker-compose -f deploy/docker-compose.yml --project-directory . build

up:
	docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . up

shell:
	docker exec -it poll_us_platform-api-1 bash
