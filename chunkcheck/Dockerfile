# pull official base image
FROM python:3.7-alpine as builder
MAINTAINER giovannt_92@hotmail.com

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY ./Requirements.txt .
RUN apk update \
	&& pip install --upgrade pip \
	&& pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r Requirements.txt

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

RUN (echo "* * * * * cd /home/app/web; /usr/local/bin/python3.7 chunk_chek.py > /var/log/cron" >> /var/spool/cron/crontabs/root)
RUN (echo "* * * * * (sleep 30; cd /home/app/web; /usr/local/bin/python3.7 chunk_chek.py ) > /var/log/cron" >> /var/spool/cron/crontabs/root)

# change to the app user
#USER app

CMD cron && tail -F /var/log/cron
#CMD python chunk_check.py
