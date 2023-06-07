[![Django-app workflow](https://github.com/SelfishRob/foodgram-project-react/actions/workflows/backend.yml/badge.svg?branch=master)](https://github.com/SelfishRob/foodgram-project-react/actions/workflows/backend.yml)

# API foodgram-project-react

## Описание:
«Продуктовый помощник»: Cайт, на котором пользователи будут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис позволит пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд. 

В проекте реализована пагинация и фильтрация, что позволяет быстрее находить нужные посты.

API разработан для передачи данных в любое приложение или на фронтенд. Так же через этот интерфейс могут работать мобильное приложение или чат-бот.

### Использованные технологии:
- Python 3.7
- Django 3.2
- DRF
- Djozer/JWT
- Docker
- Docker-compose
- NGINX
- CI and CD
- GIT Actions

## Workflow:

1. tests: Проверка на соответствие проекта PEP8 и проверка тестами с помощью: 
 flake8
 pytest
2. build_and_push_to_docker_hub: Собираем образ и отправляем на DockerHub
3. Deploy: Происходит копирование и автоматическая отправка проекта на сервер
4. send_message: При успешном деплое приходит уведомление через телеграм бота


## Установка:

Клонировать репозиторий и перейти в него в командной строке:

```
git@github.com:SelfishRob/foodgram-project-react.git
```

```
cd infra/
```
#### Шаблон наполнения infra/.env файла:

```
SECRET_KEY = 'secret_key' # Секретный ключ Django
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
```


Чтобы развернуть докер-контейнеры вручную, выполнить миграции и загрузить статику, используйте:

```
docker-compose up -d
```

Установить зависимости из файла requirements.txt:

```
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py collectstatic --no-input
```

Создание суперюзера:
```
docker-compose exec backend python manage.py createsuperuser
```

## Примеры:
Регистрация:
```
http://localhost/api/users/
```
Получение токена:
```
http://localhost/api/auth/token/login
```
Ингредиенты, теги и рецепты доступны по адресу:
```
http://localhost/api/ingredients/
http://localhost/api/tags/
http://localhost/api/recipes/
```

# Сервер:
[51.250.23.140](http://51.250.23.140)

admin:
username/password: admin1
email: admin1@admin.ru



#### Автор: **[Хафизов Роберт](https://github.com/SelfishRob)**

