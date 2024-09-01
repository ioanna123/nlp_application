# syntax=docker/dockerfile:1.4

FROM python:3.10 AS base


RUN apt-get update \
    && apt-get install -y build-essential --no-install-recommends \
    && apt-get install -y libpq-dev --no-install-recommends \
    # cleaning up unused files
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app
COPY .git .git

COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml


FROM base as app

WORKDIR /usr/src/app

RUN pip3 install --no-cache-dir poetry==1.8.2
ENV PATH = "${PATH}:/root/.poetry/bin"


# generate wheel and install application + dependencies
RUN poetry install --no-interaction

COPY . .

