# SIMPLE SOCIAL NETWORK

## Installation

Prerequisites:
- docker
- docker-compose
- git

Simply clone this repo:

```
git clone https://github.com/faked86/simple-social-network.git
cd simple-social-network
```

## Usage

- Run `docker-compose up -d` in terminal to start app in Docker.
App will work on `localhost:8080`. Database will work on `localhost:5432`.

- Run `docker-compose down` in terminal to stop app in Docker.

## Interactive docs

When app is running go to `localhost:8080/docs` or `localhost:8080/redoc` for interactive docs.

## Style guide

Used `black` formatter (line length 88 symbols), `mypy` linter.

## Tests

WIP
