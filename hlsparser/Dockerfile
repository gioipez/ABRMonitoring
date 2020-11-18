# pull official base image
FROM python:3.7-alpine as builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY ./Requirements.txt .
RUN echo nameserver 8.8.8.8 >> /etc/resolv.conf
RUN apk update \
    && apk add gcc musl-dev --no-cache \
    && pip install --upgrade pip \
    && pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r Requirements.txt

# copy project
COPY . .

#########
# FINAL #
#########
FROM python:3.7-alpine

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup -S app && adduser -S app -G app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/Requirements.txt .
RUN pip install --no-cache /wheels/*

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app
EXPOSE 8000
CMD ["gunicorn", "hlsparser.wsgi:application", "-w", "4", "--max-requests", "1200", "--timeout", "60", "--bind", "0.0.0.0:8000"]
