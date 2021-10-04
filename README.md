# api_yamdb
## REST API YaMDB - база отзывов пользователей о фильмах, книгах, музыке. 
### Технологии
- Python 3.8.5
- Django 3.0.5
- Docker-compose 3.7
- nginx 1.19.3
- postgres 12.4

### Запуск проекта 
``` docker-compose up -d --build ```

### Cоздания суперпользователя 
``` docker-compose exec web python manage.py createsuperuser ```

### Заполнения базы начальными данными
``` docker-compose exec web python manage.py loaddata fixtures.json ```
