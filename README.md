# TLDR

`make help`

# If you don't have make (?) available in your OS

All handy scripts are gathered in `Makefile` so, if you cannot use make, please just copy-paste the corresponding commands from the `Makefile`

**create dev environment**

`mkdir env && cp ./sample_dev.env ./env/dev.env`


**create prod environment**

`mkdir env && cp ./sample_prod.env ./env/prod.env`

**run dev environment**

`docker compose -f docker-compose-dev.yml up --remove-orphans`

**run prod environment**

`docker compose -f docker-compose-prod.yml up --remove-orphans`


**run tests**	
```
docker compose -f docker-compose-test.yml run --remove-orphans --rm pytest && \
docker compose -f docker-compose-test.yml down && \
docker compose -f docker-compose-test.yml rm
```

**run coverage & generate coverage report**	
```
docker compose -f docker-compose-test.yml run --remove-orphans --rm pytest coverage run -m pytest && \
docker compose -f docker-compose-test.yml run --remove-orphans --rm pytest coverage report && \
docker compose -f docker-compose-test.yml down && \
docker compose -f docker-compose-test.yml rm
```
	
**run black linter**

```
docker run --rm --volume ./src/b2broker:/src --workdir /src pyfound/black:latest_release black .
```


# Quickstart

`make sample-prod-env`

`make prod-run`


or (from `Makefile`)

`mkdir env`

`cp ./sample_prod.env ./env/prod.env`

`docker compose -f docker-compose-prod.yml up --remove-orphans`


go to http://localhost:4444/api/v1/schema/ui/

# Environments

Environments are based on env files & different docker compose files.
There are 3 environments:
- test, used for testing & coverage reports, the env file is under version control
- dev, used for development, the env file is not under version control, you have to create it manually from sample one or use Makefile
- prod, used for production, same policy for the env file, includes nginx as a front web server


## Test environment

Used for running tests, tests are implemented using pytest. The MySQL database is used because there are operations with decimals

`make tests` to run tests

`make coverage` to run the coverage report


## Dev environment

Used for the local development, runs MySQL & Django devserver on `http://localhost:8000` 

db data dir is `./dev-dbdata`

### 1. Prepare the environment

`make sample-dev-env`

OR create a dir `env` & put `dev.env` there, you can use `sample_dev.env`, it would work out of the box

### 2. Run the dev sever

`make dev-run`

go to http://localhost:8000/api/v1/schema/ui/


## Prod environment

Simulates the real production environment, has the debugging off, has the nginx which serves static files.

db data dir is `./prod-dbdata`

### 1. Prepare the environment

`make sample-prod-env`

OR create a dir `env` & put `prod.env` there, you can use `sample_prod.env`, it would work out of the box

### 2. Run the prod server

`make prod-run`

go to http://localhost:4444/api/v1/schema/ui/



# Docs

The documentation is generated dynamically via drf-spectacular and can be not perfect is some cases.


# Code linting

Run the default black (https://github.com/psf/black) to fix the code etc.

`make black`

# P.S.

tested on versions:
- docker `27.0.3` & `26.1.5`
- docker compose `2.29` & `2.29.2`
