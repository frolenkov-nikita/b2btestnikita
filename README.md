# If you don't have make (?) available in your OS

All handy scripts are gathered in `Makefile` so, if you cannot use make, please just copy-paste the corresponding commands from the `Makefile`

# Quickstart

`$ make sample-prod-env`

`$ make prod-run`


or (from `Makefile`)

`$ mkdir env`

`$ cp ./sample_prod.env ./env/prod.env`

`$ docker compose -f docker-compose-prod.yml up --remove-orphans`


go to http://localhost:4444/api/v1/schema/ui/

# Environments

Environments are based on env files & different docker compose files.
There are 3 environments:
- test, used for testing & coverage reports, the env file is under version control
- dev, used for development, the env file is not under version control, you have to create it manually from sample one or use Makefile
- prod, used for production, same as dev re: env file, includes nginx as a front web server


## Test environment

Used for running tests, tests are implemented using pytest. The MySQL database is used there because there operations with decimals

`$ make tests` to run tests

`$ make coverage` to run the coverage report


## Dev environment

Used for the local development, runs MySQL & Django runserver on `http://localhost:8000` 

### 1. Prepare the environment

`$ make sample-dev-env`

OR create a dir `env` & put `dev.env` there, you can use `sample_dev.env`, it would work out of the box

### 2. Run the dev sever

`$ make dev-run`

go to http://localhost:8000/api/v1/schema/ui/


## Prod environment

Simulates the real production environment, has the debugging off, has the nginx which servs static

### 1. Prepare the environment

`$ make sample-prod-env`

OR create a dir `env` & put `prod.env` there, you can use `sample_prod.env`, it would work out of the box

### 2. Run the dev sever

`$ make prod-run`

go to http://localhost:4444/api/v1/schema/ui/



# Docs

The documentation is dynamically generated via drf-spectacular and might be not perfect is some case.


# Code linting

run black (https://github.com/psf/black) 

`$ make black`

