# mongors1conf - сервера конфигурации; mongors1n1/mongors1n2/mongors1n3 - репликации первого шарда;
# mongors2n1/mongors2n2/mongors2n3 - репликации второго шарда; mongos1 - маршрутизатор Mongos

# Настройка серверов конфигурации
docker exec -it mongocfg1 bash -c 'echo "rs.initiate({_id: \"mongors1conf\", configsvr: true, members: [{_id: 0, host: \"mongocfg1\"}, {_id: 1, host: \"mongocfg2\"}, {_id: 2, host: \"mongocfg3\"}]})" | mongosh'
# Сборка набора реплик первого шарда
docker exec -it mongors1n1 bash -c 'echo "rs.initiate({_id: \"mongors1\", members: [{_id: 0, host: \"mongors1n1\"}, {_id: 1, host: \"mongors1n2\"}, {_id: 2, host: \"mongors1n3\"}]})" | mongosh'
# Прикрепление шарда к маршрутизаторам
docker exec -it mongos1 bash -c 'echo "sh.addShard(\"mongors1/mongors1n1\")" | mongosh'
# Инициализация репликаций
docker exec -it mongors2n1 bash -c 'echo "rs.initiate({_id: \"mongors2\", members: [{_id: 0, host: \"mongors2n1\"}, {_id: 1, host: \"mongors2n2\"}, {_id: 2, host: \"mongors2n3\"}]})" | mongosh'
# Добавление репликаций в кластер mongors2
docker exec -it mongos1 bash -c 'echo "sh.addShard(\"mongors2/mongors2n1\")" | mongosh'
# Создание тестовой БД ugc_db
docker exec -it mongors1n1 bash -c 'echo "use ugc_db" | mongosh'
# Включение шардирования в БД
docker exec -it mongos1 bash -c 'echo "sh.enableSharding(\"ugc_db\")" | mongosh'

# Создание тестовой коллекции like_dislike в БД ugc_db
docker exec -it mongos1 bash -c 'echo "db.createCollection(\"ugc_db.like_dislike\")" | mongosh'
# Настройка шардирования для коллекции like_dislike
docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"ugc_db.like_dislike\", {\"film_id\": \"hashed\"})" | mongosh'

# Создание тестовой коллекции reviews в БД ugc_db
docker exec -it mongos1 bash -c 'echo "db.createCollection(\"ugc_db.reviews\")" | mongosh'
# Настройка шардирования для коллекции reviews
docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"ugc_db.reviews\", {\"film_id\": \"hashed\"})" | mongosh'

# Создание тестовой коллекции bookmarks в БД ugc_db
docker exec -it mongos1 bash -c 'echo "db.createCollection(\"ugc_db.bookmarks\")" | mongosh'
# Настройка шардирования для коллекции bookmarks
docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"ugc_db.bookmarks\", {\"film_id\": \"hashed\"})" | mongosh'

docker exec -it mongos1 bash -c 'echo "show collections" | mongosh'
