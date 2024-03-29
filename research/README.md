# Проектная работа 9 спринта. Исследование: выбор хранилища

Цель - выбрать хранилище по результатам исследования 
и тестирования работоспособности MongoDB и ClickHouse
в части вставки и чтении информации о:
* лайках/дизлайках за фильм;
* рецензии на фильм;
* закладок с фильмом.

Тестирование вставки с разными размерами батчей (от 1 до 5000).

#### Порядок проведения тестов
1. Перейти в текущую папку research
mongo
```shell
cd research
```
2. Прописать в консоли команду сборки контейнеров
mongo
```shell
make run test_mongo_db
```
или clickhouse
```shell
make run test_clickhouse_db
```
3. Запустить процесс тестирования с помощью команды
mongo
```shell
bash ./mongo/build.sh
python -m mongo.mongodb
```
или clickhouse
```shell
python -m clickhouse.run_clickhouse.py
```


#### Результаты тестирования
1. MongoDB
##### Запись лайков/дизлайков
| Размер Батча | Время записи на батч | Время записи 1 элемента |
|:------------:|:--------------------:|:-----------------------:|
|      1       |      0.0143 сек      |       0.0143 сек        |
|      10      |      0.0095 сек      |       0.00095 сек       |
|      50      |      0.013 сек       |       0.00026 сек       |
|     100      |      0.0152 сек      |       0.00015 сек       |
|     200      |      0.0194 сек      |      0.0000973 сек      |
|     500      |      0.031 сек       |     0.00006225 сек      |
|     1000     |      0.049 сек       |      0.0000496 сек      |
|     2000     |      0.084 сек       |     0.00004226 сек      |
|     5000     |      0.223 сек       |      0.0000445 сек      |

##### Запись рецензии на фильм
| Размер Батча | Время записи на батч | Время записи 1 элемента |
|:------------:|:--------------------:|:-----------------------:|
|      1       |      0.0454 сек      |        0.454 сек        |
|      10      |      0.012 сек       |       0.00112 сек       |
|      50      |      0.0215 сек      |       0.0043 сек        |
|     100      |      0.018 сек       |       0.00018 сек       |
|     200      |       0.02 сек       |       0.0001 сек        |
|     500      |      0.0428 сек      |      0.0000856 сек      |
|     1000     |       0.06 сек       |     0.00006098 сек      |
|     2000     |      0.118 сек       |      0.0000589 сек      |
|     5000     |      0.282 сек       |      0.0000565 сек      |

##### Запись закладок
| Размер Батча | Время записи на батч | Время записи 1 элемента |
|:------------:|:--------------------:|:-----------------------:|
|      1       |      0.0148 сек      |       0.0148 сек        |
|      10      |      0.0298 сек      |       0.00298 сек       |
|      50      |      0.0138 сек      |       0.00277 сек       |
|     100      |      0.0325 сек      |       0.00033 сек       |
|     200      |      0.0198 сек      |       0.00009 сек       |
|     500      |      0.074 сек       |       0.00015 сек       |
|     1000     |      0.079 сек       |      0.000079 сек       |
|     2000     |       0.11 сек       |       0.00005 сек       |
|     5000     |       0.26 сек       |       0.00005 сек       |


2. ClickHouse
##### Запись лайков/дизлайков
| Размер Батча | Время записи на батч | Время записи 1 элемента |
|:------------:|:--------------------:|:-----------------------:|
|      1       |      20.02 сек       |        20.02 сек        |
|      10      |      20.01 сек       |          2 сек          |
|      50      |      20.01 сек       |         0.4 сек         |
|     100      |      20.01 сек       |         0.2 сек         |
|     200      |      20.01 сек       |         0.1 сек         |
|     500      |      20.06 сек       |        0.04 сек         |
|     1000     |      20.02 сек       |        0.02 сек         |
|     2000     |      20.02 сек       |        0.01 сек         |
|     5000     |      20.02 сек       |        0.004 сек        |

##### Запись рецензии на фильм
| Размер Батча | Время записи на батч | Время записи 1 элемента |
|:------------:|:--------------------:|:-----------------------:|
|      1       |      52.65 сек       |        52.65 сек        |
|      10      |      20.02 сек       |          2 сек          |
|      50      |      20.01 сек       |         0.4 сек         |
|     100      |      46.14 сек       |        0.46 сек         |
|     200      |        20 сек        |         0.1 сек         |
|     500      |        20 сек        |         0.4 сек         |
|     1000     |        20 сек        |        0.02 сек         |
|     2000     |        20 сек        |        0.01 сек         |
|     5000     |      20.02 сек       |        0.004 сек        |

##### Запись закладок
| Размер Батча | Время записи на батч | Время записи 1 элемента |
|:------------:|:--------------------:|:-----------------------:|
|      1       |        20 сек        |         20 сек          |
|      10      |        20 сек        |          2 сек          |
|      50      |      20.017 сек      |         0.4 сек         |
|     100      |      20.018 сек      |         0.2 сек         |
|     200      |      20.016 сек      |         0.1 сек         |
|     500      |      20.018 сек      |        0.04 сек         |
|     1000     |      20.018 сек      |        0.02 сек         |
|     2000     |      20.018 сек      |        0.01 сек         |
|     5000     |      20.02 сек       |        0.004 сек        |

#### Заключение
По результатам работоспособности MongoDb оказался более предпочтительным (судя по таблице).
Среднее время чтения 500 данных в Монго ~ 0.9 секунд.


## Авторы
[Polinavas95](https://github.com/Polinavas95) | <tatsuchan@mail.ru>

[Barahlush](https://github.com/Barahlush) | <baralti va@gmail.com>

