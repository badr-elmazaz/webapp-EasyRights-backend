FROM python:slim-buster AS stage1

ARG BUILD="gcc libffi-dev libc-dev python-dev"
WORKDIR /app

RUN apt-get update -y \
    && apt-get install git -y \
    && apt-get install -y wget \
    && apt install -y netcat \
    && python -m venv venv  \
    && apt-get install -y --no-install-recommends ${BUILD}


COPY . .




FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim-2021-10-02
COPY --from=stage1 /app /app


WORKDIR /app
RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install git -y

RUN pip install --no-cache-dir -r requirements.txt
RUN rm -rf requirements_prod.txt
RUN python -m compileall -b .
RUN rm -rf **/*.py
RUN rm *.py


