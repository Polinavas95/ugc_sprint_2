
test_clickhouse_db:
	docker-compose -f ./clickhouse/docker-compose.yml up --build
	python -m clickhouse.run_clickhouse.py

test_mongo_db:
	docker-compose -f ./mongo/docker-compose.yml up --build -d
	bash ./mongo/build.sh
	pip install -r requirement.txt
	python -m mongo.mongodb
