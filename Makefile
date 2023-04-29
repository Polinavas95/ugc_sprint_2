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
	cp api_ugc/etl_ugc/.env.example api_ugc/etl_ugc/.env_etl_ugc
	poetry export -f requirements.txt --output api_ugc/requirements.txt --without-hashes --without dev
	docker-compose -f api_ugc/docker-compose.yml up --build -d

run_clickhouse:
	docker-compose -f ./database/clickhouse/docker-compose.yml up --build -d

run_user_api:
	docker-compose -f ./user_api/docker-compose.yml up --build -d
	bash ./user_api/src/create_claster.sh

run_user_api_test:
	docker-compose -f ./user_api/docker-compose-test.yml up --build -d

run_elk:
	docker-compose -f ./elk/docker-compose.yml up --build -d

test:
	make run_kafka
	make run_clickhouse
	make run_elk
	make run_user_api_test
	pytest tests -k test_get_bookmarks