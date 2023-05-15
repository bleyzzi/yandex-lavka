# Задание для ШБР Yandex 2023 Python

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

## Описание

Веб-приложение, которое реализует функционал интернет-магазина. 
Функционал включает в себя возможность добавления курьеров и заказов,
распределения заказов между курьерами, рассчет зарплаты и рейтинга курьеров.

## Выполнено:
### Задание 1. REST API

Реализовано 7 методов:

Метод  | Описание
-------|---------
 `POST /couriers` | Создает новых курьеров
 `GET /couriers` | Возвращает информацию о курьерах
 `POST /orders` | Создает заказы
 `GET /orders/{order_id}` | Возвращает информацию о заказе
 `GET /orders` | Возвращает информацию о всех заказах
 `POST /orders/complete` | Отмечает, что заказ выполнен

### Задание 2. Рейтинг курьеров

Реализован один метод:

Метод  | Описание
-------|---------
`GET /couriers/meta-info/{courier_id}` | Возвращает заработанные курьером деньги за заказы и его рейтинг

### Задание 3. Rate limiter

Сервис ограничивает нагрузку в 10 RPS на каждый эндпоинт. Если допустимое количество запросов превышено, сервис отвечает кодом 429.

## Запуск

### Docker-compose
Выполнить команду

```docker-compose up -d --build```

Сервер будет доступен по адресу 8080