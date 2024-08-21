FROM python:3.12 AS python-build

# as slim doesn't have the required build deps
WORKDIR /tmp
ADD requirements.txt /tmp

RUN pip install -r requirements.txt

