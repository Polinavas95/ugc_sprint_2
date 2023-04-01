#!/usr/bin/env bash
# mongors1conf - сервера конфигурации; mongors1n1/mongors1n2/mongors1n3 - репликации первого шарда;
# mongors2n1/mongors2n2/mongors2n3 - репликации второго шарда; mongos1 - маршрутизатор Mongos

# Настройка серверов конфигурации
docker exec mongocfg1 bash -c 'echo "rs.initiate({_id: \"mongors1conf\", configsvr: true, members: [{_id: 0, host: \"mongocfg1\"}, {_id: 1, host: \"mongocfg2\"}]})" | mongo'

# Сборка набора реплик первого шарда
docker exec mongors1n1 bash -c 'echo "rs.initiate({_id: \"mongors1\", members: [{_id: 0, host: \"mongors1n1\"}, {_id: 1, host: \"mongors1n2\"}]})" | mongo'
# Сборка набора реплик второго шарда
docker exec mongors2n1 bash -c 'echo "rs.initiate({_id: \"mongors2\", members: [{_id: 0, host: \"mongors2n1\"}, {_id: 1, host: \"mongors2n2\"}]})" | mongo'

sleep 20

# Прикрепление первого шарда к маршрутизаторам
docker exec mongos1 bash -c 'echo "sh.addShard(\"mongors1/mongors1n1\")" | mongo'
# Прикрепление второго шарда к маршрутизаторам
docker exec mongos1 bash -c 'echo "sh.addShard(\"mongors2/mongors2n1\")" | mongo'

# Создание тестовой БД ugc_db
docker exec mongors1n1 bash -c 'echo "use ugc_db" | mongo'

# Включение шардирования в БД
docker exec mongos1 bash -c 'echo "sh.enableSharding(\"ugc_db\")" | mongo'

# Создание тестовой коллекции movie_likes в БД ugc_db
docker exec -it mongos1 bash -c 'echo "db.createCollection(\"ugc_db.movie_likes\")" | mongosh'
# Настройка шардирования для коллекции movie_likes
docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"ugc_db.movie_likes\", {\"film_id\": \"hashed\"})" | mongosh'

# Создание тестовой коллекции user_bookmarks в БД ugc_db
docker exec -it mongos1 bash -c 'echo "db.createCollection(\"ugc_db.user_bookmarks\")" | mongosh'
# Настройка шардирования для коллекции user_bookmarks
docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"ugc_db.user_bookmarks\", {\"film_id\": \"hashed\"})" | mongosh'

# Создание тестовой коллекции user_bookmarks в БД ugc_db
docker exec -it mongos1 bash -c 'echo "db.createCollection(\"ugc_db.user_bookmarks\")" | mongosh'
# Настройка шардирования для коллекции user_bookmarks
docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"ugc_db.user_bookmarks\", {\"film_id\": \"hashed\"})" | mongosh'

docker exec -it mongos1 bash -c 'echo "show collections" | mongosh'
