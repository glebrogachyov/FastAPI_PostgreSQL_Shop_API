# Микросервис "База данных интернет-магазина"

#### FastAPI, PostgreSQL, SQLAlchemy
## Порядок установки:

1. Скачать папку с проектом
2. Открыть в Pycharm папку проекта, подтвердить создание виртуального окружения и установку зависимостей из requirements.txt
3. В конфигурации "script path" указать путь к файлу "app/main.py"
4. Если требуется, тогда указать в файле ".env" настройки БД Postgres (по умолчанию установлен порт "5432", пароль "mysecretpassword", имя пользователя и БД - "postgres")

___

## Тестовый сценарий:

1. Запустить проект кнопкой RUN из Pycharm - будет запущен сервер Uvicorn и автоматически создадутся таблицы product и cart.

2. Добавить в базу данных два товара "Смартфон Google Pixel" с разным объёмом памяти с помощью POST-запросов:
```sh
curl -X 'POST' \
  'http://localhost:8000/products' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Смартфон Google Pixel 64GB",
  "price": 50000,
  "description": "Google Pixel 64GB with Pure Android"
}'
```
```sh
curl -X 'POST' \
  'http://localhost:8000/products' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Смартфон Google Pixel 128GB",
  "price": 55000,
  "description": "Google Pixel 128GB with Pure Android"
}'
```

3. Для поиска в по слову "Pixel" выполнить следующий запрос:
```sh
curl -X 'GET' \
  'http://localhost:8000/products?names=Pixel' \
  -H 'accept: application/json'
```

4. Получить детальное описание товара с id=2:
```sh
curl -X 'GET' \
  'http://localhost:8000/products/2' \
  -H 'accept: application/json'
```



___

## Дополнительные тесты:
Для полноценного тестирования API можно открыть в браузере страницу с OpenAPI документацией: http://localhost:8000/ 
Наполнить таблицу данными, отправив POST-запрос init_tables, и оценить работу реализованных методов.
После всех тестов метод drop_tables удалит созданные таблицы, эти методы писались для удобства разработки, но я решил их оставить и для более простого тестирования.

![](/images/methods.JPG)
