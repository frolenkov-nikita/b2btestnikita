all: help

help:
	@echo "sample-dev-env				- Create sample environment for dev. purposes"
	@echo "sample-prod-env				- Create sample environment for prod. purposes"
	@echo "dev-run					 	- Launch development docker compose"
	@echo "prod-run					 	- Launch production docker compose"
	@echo "tests                        - Run pytest tests using docker compose."
	@echo "coverage                     - Create coverage report."


sample-dev-env:
	-@mkdir env
	-@cp ./sample_dev.env ./env/dev.env

sample-prod-env:
	-@mkdir env
	-@cp ./sample_prod.env ./env/prod.env

dev-run:
	-@docker compose -f docker-compose-dev.yml up --remove-orphans

prod-run:
	-@docker compose -f docker-compose-prod.yml up --remove-orphans

tests:
	-@docker compose -f docker-compose-test.yml run --remove-orphans --rm pytest
	-@docker compose -f docker-compose-test.yml down
	-@docker compose -f docker-compose-test.yml rm

coverage:
	@docker compose -f docker-compose-test.yml run --remove-orphans --rm pytest coverage run -m pytest
	@docker compose -f docker-compose-test.yml run --remove-orphans --rm pytest coverage report
	-@docker compose -f docker-compose-test.yml down
	-@docker compose -f docker-compose-test.yml rm

black:
	@docker run --rm --volume ./src/b2broker:/src --workdir /src pyfound/black:latest_release black .
