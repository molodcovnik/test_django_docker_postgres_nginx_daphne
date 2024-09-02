## Лента сообщений с почты


### Скачиваем репозиторий

`git clone https://github.com/molodcovnik/test_django_docker_postgres_nginx_daphne.git`

### 1. Запускаем в Docker

Убедитесь, что у вас установлен `docker` и `docker-compose` последних версий

1. `docker-compose up --build`

2. Дожидаемся старта

3. Заходим по урл localhost БЕЗ ПОРТА !


### 2. Запускаем локально без Docker

#### Раскомментировать CHANNEL_LAYERS, DATABASES, STATIC_URL, STATICFILES_DIRS в файле settings.py которые предназначены для локального запуска 
#### Закомментировать CHANNEL_LAYERS, DATABASES, STATIC_URL, STATICFILES_DIRS, STATIC_ROOT в файле settings.py которые предназначены для докер окружения

#### Открываем терминал и вводим следующие команды

    `redis-server`

#### Открываем еще один терминал и вводим следующие команды

```
    cd test_django_docker_postgres_nginx_daphne
    python3 -m venv venv
    source ./venv/bin/activate
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py runserver
```

1. Заходим по урл 127.0.0.1:8000 



### Видео-пример как работает приложение

https://disk.yandex.ru/d/Bz7-2y2o4nUOrQ
