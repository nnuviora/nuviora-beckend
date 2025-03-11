poetry add fastapi

poetry add uvicorn[standard]

poetry add sqlalchemy
poetry add psycopg2
poetry add alembic

├── src
|  ├─database
│  |   ├── db.py
│  |   └── models.py
│  ├── repository
│  |   ├── notes.py
│  |   └── tags.py
│  ├── routes
│  |   ├── notes.py
│  |   └── tags.py
│  └── schemas.py
├── pyproject.toml
└── main.py

Точка входу в наш застосунок - main.py, а всередині папки src ми помістимо файли для роботи з нашим застосунком.

Кожен файл буде мати свою зону відповідальності:

repository/notes.py, repository/tags.py - додатковий шар абстракції, який містить методи для роботи з базою даних.
Кожен файл відповідає за роботу із конкретною таблицею.
database/db.py - буде відповідати за підключення до бази даних PostgreSQL
database/models.py - буде містити наші моделі бази даних
routes/notes.py, routes/tags.py - тут будуть знаходитись маршрути нашого REST API застосунку,
для роботи з нашими сутностями – нотатками (notes) та тегами (tags).
Звідси ми будемо викликати методи репозиторію, а не звертатись до бази даних напряму
schemas/notes.py - схеми для валідації наших вхідних та вихідних даних

docker run --name rest_app -p 5432:5432 -e POSTGRES_PASSWORD=567234 -d postgres

src/database/db.py
src/database/models.py


alembic init migrations

migrations/env.py    отредактировать файл env.py, в папке migrations, согласно описания в лекции

alembic revision --autogenerate -m 'Init'
    Якщо файл з міграцією успішно створився в папці migrations/versions, то:
alembic upgrade head

src/schemas.py

Щоб реалізувати повний цикл CRUD операцій, нам необхідно реалізувати набір маршрутів нашого REST API застосунку:
Отримати список усіх тегів: маршрут - /api/tags, HTTP метод GET
Створити тег: маршрут - /api/tags, HTTP метод POST
Отримати тег за id: маршрут - /api/tags/<int:id>, HTTP метод GET
Оновити тег: маршрут - /api/tags/<int:id>, HTTP метод PUT
Видалити тег: маршрут - /api/tags/<int:id>, HTTP метод DELETE

add in main.py

src/routes/tags.py

src/repository/tags.py

Робота з нотатками будується аналогічно до роботи з тегами:
Отримати список нотаток: маршрут - /api/notes, HTTP метод GET
Створити нотатку: маршрут - /api/notes, HTTP метод POST
Отримати нотатку за id: маршрут - /api/notes/<int:id>, HTTP метод GET
Оновити статус нотатки: маршрут - /api/notes/<int:id>, HTTP метод patch
Видалити нотатку: маршрут - /api/notes/<int:id>, HTTP метод DELETE

src/routes/notes.py

src/repository/notes.py


uvicorn main:app --host localhost --port 8000 --reload


module 12

poetry add libgravatar
poetry add python-jose["cryptography"]
poetry add passlib["bcrypt"]
poetry add python-multipart

uvicorn main:app --host localhost --port 8000 --reload

edit src/database/models.py
edit src/schemas.py
src/repository/users.py
src/services/auth.py

src/routes/auth.py

in main.py add:
app.include_router(auth.router, prefix='/api')

edit src/repository/tags.py
edit src/repository/notes.py

edit src/routes/tags.py
edit src/routes/notes.py


alembic revision --autogenerate -m 'Init'
alembic upgrade head

user: admin@ex.ua 567234

Простые шаги для отключения проекта от текущего репозитория
Если вы хотите отключить свой проект от текущего репозитория, следуйте этим простым шагам:

Откройте терминал или командную строку.
Перейдите в папку проекта, используя команду cd.
Скопируйте URL репозитория, с которого вы хотите отключиться.
Введите команду git remote -v, чтобы увидеть список всех удаленных репозиториев.
Используйте команду git remote remove [имя репозитория], чтобы удалить ссылку на репозиторий, от которого вы хотите отключиться. Например, если имя удаленного репозитория «origin», введите git remote remove origin.
Для подтверждения выполните команду git remote -v еще раз и убедитесь, что репозиторий был успешно удален.

module13
test9095945@meta.ua Q1w2....
poetry add fastapi-mail

views environ
import os
api_key = os.environ.get('API_KEY')

load environ
from dotenv import load_dotenv
load_dotenv()

poetry add python-dotenv

.env

src/conf/config.py

Змінюємо моделі та репозиторій (don`t forgot migrations)
in scr/repository/users.py
scr/services/email.py
in scr/services/auth.py
scr/services/templates/email_template.html

Змінюємо роботу маршрутів
in scr/routes/auth.py (signup, login, confirmed)
in scr/services/auth.py (auth_service.get_email_from_token)
in scr/routes/auth.py (request_email)
in scr/schemas.py (request_email)

alsol@i.ua 567234

docker-compose up -d  (rest-app, redis-cache)

poetry add fastapi-limiter
in main.py
in scr/routes/notes.py

 poetry add cloudinary
 in scr/repository/users.py (update_avatar)
 scr/routes/users.py
 in main.py (add users)

Modele 14

plagin PyCharm Trelent - AI Docstrings on Demand (alt+D in funktion)

poetry add sphinx -G dev
sphinx-quickstart docs (quetions)
cd docs
edit docs/conf.py
edit docs/index.rst

test14@ua.fm 567234

testing

md tests
tests\test_unit_repository_notes.py
python -m unittest .\tests\test_unit_repository_notes.py

poetry add pytest -G dev
poetry add httpx

poetry add pytest_asyncio

pytest tests/ -s


Cloudinary

poetry add cloudinary

 "username": "test14",
  "email": "test14@ex.ua",
  "password": "567234"


