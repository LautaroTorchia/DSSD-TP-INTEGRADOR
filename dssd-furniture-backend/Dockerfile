###########
# BUILDER #
###########

# pull official base image
FROM python:3.9.6-alpine as builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev yaml-dev

COPY . .
#RUN flake8 --ignore=E501,F401 .

# install dependencies
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


#########
# FINAL #
#########

# pull official base image
FROM python:3.9.6-alpine

# set environment variables
ARG POSTGRES_DB
ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG SQL_HOST
ARG SQL_PORT
ARG SECRET_KEY
ARG DJANGO_HOSTS
ARG EMAIL_HOST_USER
ARG EMAIL_HOST_PASSWORD
ARG PARAMETER_NIFI_HOST


ENV DEBUG 0
ENV SECRET_KEY=$SECRET_KEY
ENV DJANGO_ALLOWED_HOSTS=$DJANGO_HOSTS
ENV SQL_ENGINE tenant_schemas.postgresql_backend
ENV POSTGRES_DB=$POSTGRES_DB
ENV POSTGRES_USER=$POSTGRES_USER
ENV POSTGRES_PASSWORD=$POSTGRES_PASSWORD
ENV SQL_HOST=$SQL_HOST
ENV SQL_PORT=$SQL_PORT
ENV DATABASE postgres
ENV EMAIL_HOST_USER=$EMAIL_HOST_USER
ENV EMAIL_HOST_PASSWORD=$EMAIL_HOST_PASSWORD
ENV parameter_nifi_HOST $PARAMETER_NIFI_HOST

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup -S app && adduser -S app -G app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/mediafiles
WORKDIR $APP_HOME

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

RUN apk update && apk add libpq

# change to the app user
USER app

# install dependencies
ENV PATH="/home/app/.local/bin:${PATH}"
RUN python -m pip install --user --upgrade pip
RUN pip install --no-cache-dir --upgrade pip
COPY --chown=app:app --from=builder /usr/src/app/wheels /wheels
COPY --chown=app:app --from=builder /usr/src/app/requirements.txt .
RUN pip install --user --no-cache /wheels/*

# copy entrypoint.prod.sh
COPY ./entrypoint.prod.sh .
RUN sed -i 's/\r$//g'  $APP_HOME/entrypoint.prod.sh
RUN chmod +x  $APP_HOME/entrypoint.prod.sh

# run entrypoint.prod.sh
RUN chmod 0700 /home/app/web/entrypoint.gunicorn.sh
ENTRYPOINT ["/home/app/web/entrypoint.gunicorn.sh"]
