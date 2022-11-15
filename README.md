![foodgram_workflow](https://github.com/SKhnykin/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
# Продуктовый помощник Foodgram

## Описание проекта Foodgramcd
«Продуктовый помощник»: приложение, на котором пользователи публикуют рецепты, подписываться на публикации других авторов и добавлять рецепты в избранное. Сервис «Список покупок» позволит пользователю создавать список продуктов, которые нужно купить для приготовления выбранных блюд.


## Запуск проекта через Docker
- В папке infra выполнить команду, что бы собрать контейнер:
```bash
sudo docker-compose up -d
```

Для доступа к контейнеру выполните следующие команды:

```bash
sudo docker-compose exec backend python manage.py makemigrations
```
```bash
sudo docker-compose exec backend python manage.py migrate --noinput
```
```bash
sudo docker-compose exec backend python manage.py createsuperuser
```
```bash
sudo docker-compose exec backend python manage.py collectstatic --no-input
```

Дополнительно можно наполнить DB ингредиентами и тэгами:

```bash
sudo docker-compose exec backend python manage.py load_tags
```
```bash
sudo docker-compose exec backend python manage.py load_ingrs
```

## Запуск проекта в dev-режиме

- Установить и активировать виртуальное окружение

```bash
source /venv/bin/activated
```

- Установить зависимости из файла requirements.txt

```bash
python -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```

- Выполнить миграции:

```bash
python manage.py migrate
```

- В папке с файлом manage.py выполнить команду:
```bash
python manage.py runserver
```

.env должен содержать:
```python
DB_ENGINE='django.db.backends.postgresql'
DB_NAME=
POSTGRES_USER=
POSTGRES_PASSWORD=
DB_HOST=db
DB_PORT='5432'
SECRET_KEY=
ALLOWED_HOSTS=
```
## Примеры

Примеры API запросов:

- [GET] - Получить список всех пользователей.
```
/api/users/
```
ответ: 200
```
{
  "count": 123,
  "next": "http://foodgram.example.org/api/users/?page=4",
  "previous": "http://foodgram.example.org/api/users/?page=2",
  "results": [
    {
      "email": "user@example.com",
      "id": 0,
      "username": "string",
      "first_name": "Вася",
      "last_name": "Пупкин",
      "is_subscribed": false
    }
  ]
}
```
- [POST] /api/users/ - Регистрация пользователя.
```
/api/users/
```
запрос:
```
{
    "email": "vpupkin@yandex.ru",
    "username": "vasya.pupkin",
    "first_name": "Вася",
    "last_name": "Пупкин",
    "password": "Qwerty123"
}
```
ответ: 201
```
{
    "email": "vpupkin@yandex.ru",
    "id": 0,
    "username": "vasya.pupkin",
    "first_name": "Вася",
    "last_name": "Пупкин"
}
```

### Весь перечень API доступен в документации.
```url
http://127.0.0.1/api/docs/
```

