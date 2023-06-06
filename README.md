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

## Установка:

Клонировать репозиторий и перейти в него в командной строке:

```
git@github.com:SelfishRob/foodgram-project-react.git
```

```
cd backend/api_foodgram
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```


## Примеры:
Регистрация:
```
http://127.0.0.1:8000/api/users/
```
Получение токена:
```
http://127.0.0.1:8000/api/auth/token/login
```
Ингредиенты, теги и рецепты доступны по адресу:
```
http://127.0.0.1:8000/api/ingredients/
http://127.0.0.1:8000/api/tags/
http://127.0.0.1:8000/api/recipes/
```
Полная документация доступна после выполнения команды 
``` docker-compose up ``` в папке инфра
```
Проект запустится на адресе http://localhost, увидеть спецификацию API вы сможете по адресу http://localhost/api/docs/
```
#### Автор: **[Хафизов Роберт](https://github.com/SelfishRob)**

