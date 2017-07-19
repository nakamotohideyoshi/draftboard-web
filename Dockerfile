FROM python:3.5.1-alpine
ENV PYTHONUNBUFFERED 1

# dir for python app
RUN mkdir /code
WORKDIR /code

RUN apk update
# install req for python modules using gcc
RUN apk add python3-dev build-base --update-cache
RUN apk add make libffi-dev openssl-dev

# update with needed outside repositories
RUN echo "@main33 http://dl-cdn.alpinelinux.org/alpine/v3.3/main" >> /etc/apk/repositories
RUN apk update

# install req for python modules using postgres
# force this to 9.4 to match kiasaki/alpine-postgres:9.4
RUN apk add "postgresql@main33<9.5" "postgresql-dev@main33<9.5" "postgresql-client@main33<9.5"

# install these for python req that use git
RUN apk add git

# dumb-init https://github.com/Yelp/dumb-init
RUN pip install dumb-init

# install python req
RUN mkdir /code/requirements
COPY requirements/_base.txt /code/requirements/
COPY requirements/local.txt /code/requirements/
RUN pip install -r requirements/local.txt

# add in useful commands into shell history
COPY docker-services/django/.ash_history /root/.ash_history

# point `python3` to `python`
RUN echo "alias python='python3'" >> /etc/profile.d/draftboard.sh

# placing this last as it is a run time variable
ARG DRAFTBOARD_SETTINGS
ENV DJANGO_SETTINGS_MODULE ${DRAFTBOARD_SETTINGS}

# by setting these, we can run `psql` by itself, as well as ref env var in django
# see http://goo.gl/fNG8Do, section `Environment`, for more information
ENV PGHOST postgres
ENV PGUSER postgres
