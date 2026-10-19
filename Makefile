PYTHON ?= python3
VENV := .venv
BIN := $(VENV)/bin

.PHONY: help install api web test test-backend test-frontend build contract migrate e2e

help:
	@echo "install: install dependencies; api/web: run servers in separate terminals"
	@echo "test: unit/API tests; build: frontend production build; contract: validate OpenAPI"
	@echo "migrate: upgrade database; e2e: run browser tests (see README prerequisites)"

install:
	$(PYTHON) -m venv $(VENV)
	$(BIN)/python -m pip install -r backend/requirements.txt
	npm --prefix frontend ci

api:
	$(BIN)/uvicorn backend.app.main:app --host 127.0.0.1 --port 8000

web:
	npm --prefix frontend run dev -- --host 127.0.0.1

test: test-backend test-frontend

test-backend:
	$(BIN)/python -m pytest backend/tests -q

test-frontend:
	npm --prefix frontend test

build:
	npm --prefix frontend run build

contract:
	$(BIN)/python -m openapi_spec_validator openapi.yml

migrate:
	$(BIN)/alembic -c backend/alembic.ini upgrade head

e2e:
	cd frontend && npx playwright test
