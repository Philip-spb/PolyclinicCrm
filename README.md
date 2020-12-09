# Форма записи к врачу в поликлинике

### Инструкция по разворачиванию приложения в контейнере docker

Запускаем команду `docker-compose up -d`

Данная команда запустит контейнер с образом системы, создаст суперпользователя (логин `admin`, пароль `pass`), а также добавит двух докторов в базу для удобства тестирования.

### Инструкция по запуску тестирования приложения

После запуска контейнера с приложением выполняем команду `docker-compose exec web ./manage test`

Данный тест создает доктора в базе и производит запись к нему пациента

## Использование приложения

Форма записи в поликлинику доступна по адресу http://127.0.0.1:8000/

В форме производится последовательный выбор:
1. Врача
2. Даты (с понедельника по пятницу)
3. Времени (с 9:00 до 18:00)

После этого пользователь указывает свое имя и производит бронирование.

Забронированное время у врача забронировать повторно невозможно.

Вход в административную панель производится по адресу http://127.0.0.1:8000/admin/ (логин и пароль указаны выше)

Администратор имеет возможность зайти в административной панели на страницу конкретного доктора и посмотреть все записи к нему. Отображаются только актуальные записи (на даты начиная с текущей).