FROM praekeltfoundation/django-bootstrap:py3.6

COPY . /app

RUN pip install -e .

# temporary untill there is a new PyCap Release
ENV DJANGO_SETTINGS_MODULE "config.settings.production"
RUN SECRET_KEY=placeholder ALLOWED_HOSTS=placeholder python manage.py collectstatic --noinput
CMD ["config.wsgi:application"]