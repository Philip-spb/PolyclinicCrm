FROM python:3.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

RUN pip install django==3.1.4

COPY . /code/
RUN ./manage.py collectstatic
RUN ./manage.py migrate
RUN ./manage.py shell -c "from django.contrib.auth.models import User; from crm.models import Doctors; User.objects.create_superuser('admin', 'admin@example.com', 'pass'); Doctors.objects.create(name='Иванов Иван Иванович'); Doctors.objects.create(name='Петров Петр Петрович')"