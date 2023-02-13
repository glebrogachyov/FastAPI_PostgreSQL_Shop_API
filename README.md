# Микросервис "База данных интернет-магазина"

#### FastAPI, PostgreSQL, SQLAlchemy
## Порядок установки:

1. Скачать папку с проектом
2. Открыть в Pycharm папку проекта, подтвердить создание виртуального окружения и установку зависимостей из requirements.txt
3. Если требуется, тогда изменить в файле ".env" настройки БД Postgres (по умолчанию установлен порт "5432", пароль "mysecretpassword", имена пользователя и БД - "postgres")

___

## Тестовый сценарий:

1. Запустить проект командой 
```sh
python main.py -init True
```
при этом автоматически создадутся таблицы product и cart, в таблицу product будут внесены 8 товаров.

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

4. Получить детальное описание товара с id=10 (т.к. 8 записей было добавлено при инициализаци):
```sh
curl -X 'GET' \
  'http://localhost:8000/products/2' \
  -H 'accept: application/json'
```



___

## Дополнительные тесты:
Для полноценного тестирования API можно открыть в браузере страницу с OpenAPI документацией: http://localhost:8000/ и оценить работу реализованных методов.
Проверить ответы сервиса при отсутствии таблиц можно послав запрос на их удаление - метод drop_tables.
Методы init_tables и drop_tables писались для удобства разработки, а не для финального результата, но я решил их оставить для более полноценного тестирования.

![](/images/methods.JPG)
