# Crypto & Stocks & FX Dashboard API

## Описание

REST API сервис для получения, хранения и аналитики котировок криптовалют, акций и курса валют.

## Запуск

1. `docker-compose up --build`
2. API доступен на [localhost:8000/docs](http://localhost:8000/docs)
3. Доступны DashBoard для просмотра аналитики запросов по символам на Flask и Django

## Тесты

```
docker-compose run api pytest
```
