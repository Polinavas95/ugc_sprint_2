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
	docker-compose -f ./database/kafka_broker/docker-compose.yml up --build -d
	poetry run python3 ./database/kafka_broker/kafka_utils/setup_kafka.py
	

run_api_ugc:
	cp api_ugc/.env.example api_ugc/.env_ugc
	poetry export -f requirements.txt --output api_ugc/requirements.txt --without-hashes --without dev
	docker-compose -f api_ugc/docker-compose.yml up --build -d

run_clickhouse:
	docker-compose -f ./database/clickhouse/docker-compose.yml up

run_etl_ugc:
	cp api_ugc/etl_ugc/.env.example api_ugc/etl_ugc/.env_etl_ugc
	docker-compose -f api_ugc/etl_ugc/docker-compose.yml up --build -d
