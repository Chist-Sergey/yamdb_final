# yamdb_final

![yamdb_final workflow](https://github.com/Chist-Sergey/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)


Это API проекта api_yamdb, который собирает отзывы (Review) пользователей на произведения (Title). Произведения делятся на категории (Category). В каждой категории есть произведения: книги, фильмы или музыка. Произведению может быть присвоен жанр (Genres) из списка предустановленных. Новые жанры может создавать только администратор.

---

Настроен Continuous Integration и Continuous Deployment для проекта YaMDB: автоматический запуск тестов, обновление образов на Docker Hub и автоматический деплой на боевой сервер при пуше в ветку main

---
### Технологии
- Python 3.8.5
- Django 3.0.5
- Docker-compose 3.7
- nginx 1.19.3
- postgres 12.4


<h3> Установка и развертывание </h3>
После выполнения push необходимо зайти на сервер

    $ ssh yc-user@<IP адрес>


### Установка докер
https://docs.docker.com/engine/install/

### Запуск проекта 
``` docker-compose up -d --build ```Shell

### Создание миграций приложения пользователей
```docker-compose exec web python manage.py makemigrations users```Shell

### Миграции
```docker-compose exec web python manage.py migrate --noinput```Shell

### Сбор статики
```docker-compose exec web python manage.py collectstatic --no-input```Shell

### Cоздания суперпользователя 
``` docker-compose exec web python manage.py createsuperuser ```Shell

### Заполнения базы начальными данными
``` docker-compose exec web python manage.py loaddata fixtures.json ```Shell

### Работал над проектом: Serega Nu Serega - ученик Яндекс.Практикум
https://hub.docker.com/repository/docker/Chist-Sergey/yamdb_final - dockerhub - dockerhub

http://84.201.162.161/admin/login/?next=/admin/ - облако 
