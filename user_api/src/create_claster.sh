#!/usr/bin/env bash
# mongors1conf - сервера конфигурации; mongors1n1/mongors1n2/mongors1n3 - репликации первого шарда;
# mongors2n1/mongors2n2/mongors2n3 - репликации второго шарда; mongos1 - маршрутизатор Mongos

# Настройка серверов конфигурации
docker exec -it mongocfg1 bash -c 'echo "rs.initiate({_id: \"mongors1conf\", configsvr: true, members: [{_id: 0, host: \"mongocfg1\"}, {_id: 1, host: \"mongocfg2\"}, {_id: 2, host: \"mongocfg3\"}]})" | mongosh'

# Сборка набора реплик первого шарда
docker exec -it mongors1n1 bash -c 'echo "rs.initiate({_id: \"mongors1\", members: [{_id: 0, host: \"mongors1n1\"}, {_id: 1, host: \"mongors1n2\"}, {_id: 2, host: \"mongors1n3\"}]})" | mongosh'

# Сборка набора реплик второго шарда
docker exec -it mongors2n1 bash -c 'echo "rs.initiate({_id: \"mongors2\", members: [{_id: 0, host: \"mongors2n1\"}, {_id: 1, host: \"mongors2n2\"}, {_id: 2, host: \"mongors2n3\"}]})" | mongosh'
sleep 20

# Прикрепление первого шарда к маршрутизаторам
docker exec -it mongos1 bash -c 'echo "sh.addShard(\"mongors1/mongors1n1\")" | mongosh'

# Прикрепление второго шарда к маршрутизаторам
docker exec -it mongos1 bash -c 'echo "sh.addShard(\"mongors2/mongors2n1\")" | mongosh'

# Создание тестовой БД ugc_db
docker exec -it mongors1n1 bash -c 'echo "use ugc_db" | mongosh'

# Включение шардирования в БД
docker exec -it mongos1 bash -c 'echo "sh.enableSharding(\"ugc_db\")" | mongosh'

# Создание тестовой коллекции movie_likes в БД ugc_db
docker exec -it mongos1 bash -c 'echo "db.createCollection(\"ugc_db.movie_likes\")" | mongosh'
# Настройка шардирования для коллекции movie_likes
docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"ugc_db.movie_likes\", {\"film_id\": \"hashed\"})" | mongosh'

# Создание тестовой коллекции user_reviews в БД ugc_db
docker exec -it mongos1 bash -c 'echo "db.createCollection(\"ugc_db.user_reviews\")" | mongosh'
# Настройка шардирования для коллекции user_reviews
docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"ugc_db.user_reviews\", {\"film_id\": \"hashed\"})" | mongosh'

# Создание тестовой коллекции user_bookmarks в БД ugc_db
docker exec -it mongos1 bash -c 'echo "db.createCollection(\"ugc_db.user_bookmarks\")" | mongosh'
# Настройка шардирования для коллекции user_bookmarks
docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"ugc_db.user_bookmarks\", {\"film_id\": \"hashed\"})" | mongosh'

docker exec -it mongos1 bash -c 'echo "show collections" | mongosh'
