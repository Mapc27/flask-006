# flask-006

## Установка и запуск проекта

- `poetry install` - создать виртуальное окружение
- установите PostgreSQL
- `sudo -i -u postgres` - зайти в консоль postgres. При необходимости, авторизоваться
- `psql`
- `CREATE DATABASE flask_app;` - создание базы данных
- `\q;` - выход из psql
- `psql -f [путь до репозитория]/flask-006/flask_006/db_schema.sql flask_app` - создание таблиц
- `config.py` - измените файл конфигурации
- `python3 flaskapp.py` - запуск сервера