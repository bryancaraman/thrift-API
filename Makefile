.PHONY: help start stop test status prune logs gen_diagrams

.DEFAULT: help
help:
	@echo "make start"
	@echo "	   Run the api and postgres, and the tests in the background. Kill it with 'make stop'. Check on it with 'make status'."
	@echo "make status"
	@echo "	   Essentially just runs 'docker-compose ps', but it's a shorter way to do it."
	@echo "make test"
	@echo "	   Start application and run the tests!"
	@echo "make logs"
	@echo "	   Follow all logs in real time. ctrl+C to stop"
	@echo "make stop"
	@echo "	   Kill the api, postgres, and the tests if they are running in the background."
	@echo "make prune"
	@echo "	   Reset database state. Run if your database is broken.. or just cluttered"
	@echo "make gen_diagrams"
	@echo "	   Run the code to generate diagrams for our project"


ifeq ($(API_PORT),)
export API_PORT := 8000
endif
# $(info API_PORT set to $(API_PORT). Change it with 'export API_PORT=')

ifeq ($(API_CLEAR_DB),)
export API_CLEAR_DB := false
endif
# $(info API_CLEAR_DB set to $(API_CLEAR_DB). Change it with 'export API_CLEAR_DB=')

start: _create_env_file _docker_run_develop_mode _remove_env_file
	@echo "The API is still running, kill it with 'make stop'. Check it's status with 'make status'."

stop: _docker_stop_api_detached

status:
	docker-compose ps

test: _create_env_file _pytest_docker _remove_env_file

logs:
	docker-compose logs -f

prune: _docker_stop_api_detached
	docker volume rm 2021bootcamp-api_postgresdb

gen_diagrams:
	docker-compose run api python /diagrams/gen_diagrams.py
	ls diagrams/*.png | xargs open

_pytest_docker:
	docker-compose --env-file /tmp/cart_api.env up --build --exit-code-from tests --abort-on-container-exit tests

_create_env_file:
	env | grep API_ > /tmp/cart_api.env

_remove_env_file:
	rm /tmp/cart_api.env

_docker_run_develop_mode:
	docker-compose --env-file /tmp/cart_api.env up --build --force-recreate -d api

_docker_stop_api_detached:
	docker-compose down || echo "Eyes up, check docker logs"
