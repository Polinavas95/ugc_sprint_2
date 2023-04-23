lint:
	@echo
	poetry run ruff .
	@echo
	poetry run blue --check --diff --color .
	@echo
	poetry run mypy .
	@echo
	poetry run pip-audit

run_kafka:
	docker-compose -f database/kafka_broker/docker-compose.yml up --build -d
	poetry run python3 database/kafka_broker/kafka_utils/setup_kafka.py
	

run_clickhouse:
	docker-compose -f database/clickhouse/docker-compose.yml up

run_api_ugc:
	cp api_ugc/.env.example api_ugc/.env_ugc
	cp api_ugc/etl_ugc/.env.example api_ugc/etl_ugc/.env_etl_ugc
	poetry export -f requirements.txt --output api_ugc/requirements.txt --without-hashes --without dev
	docker-compose -f api_ugc/docker-compose.yml up --build -d

run_elk:
	docker-compose -f elk/docker-compose.yml up

run_user_api:
	cp user_api/src/app/.env.example user_api/src/app/.env_user_api
	docker-compose -f user_api/docker-compose.yml up
	bash user_api/src/create_claster.sh
