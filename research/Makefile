
test_clickhouse_db:
	docker-compose -f ./clickhouse/docker-compose.yml up --build

test_mongo_db:
	docker-compose -f ./mongo/docker-compose.yml up --build
	bash ./mongo/build.sh
	pip install -r requirement.txt
