# flask-006

## Установка и запуск проекта

- `git clone https://github.com/Mapc27/flask-006.git` - клонирование репозитория
- `cd flask-006`
- `poetry install` - создание виртуального окружения и установка зависимостей
-  установите PostgreSQL
- `sudo -i -u postgres` - вход в консоль postgres. При необходимости, нужно авторизоваться
- `psql`
- `CREATE DATABASE flask_app;` - создание базы данных
- `\q;` - выход из psql
- `psql -f [путь до репозитория]/flask-006/flask_006/db_schema.sql flask_app` - создание таблиц
- `exit` - выход из консоли postgres
- `cd flask_006/`
- `subl config.py` или `pycharm-professional config.py` - измените файл конфигурации
- `poetry shell` - вход в виртуальное окружение
- `python3 flaskapp.py` - запуск сервера
