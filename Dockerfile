FROM frolvlad/alpine-python3
ENV PYTHONUNBUFFERED 1

# dir for python app
RUN mkdir /code
WORKDIR /code

# install req for python modules using gcc
RUN apk add python3-dev build-base --update-cache
RUN apk add make libffi-dev openssl-dev

# install req for python modules using postgres
RUN apk add postgresql-dev

# install these for python req that use git
RUN apk add git

# install python req
RUN mkdir /code/requirements
COPY requirements/_base.txt /code/requirements/
COPY requirements/local.txt /code/requirements/
RUN pip install -r requirements/local.txt

# add in useful commands into shell history
COPY docker-services/django/.ash_history /root/.ash_history

# point `python3` to `python`
RUN echo "alias python='python3'" >> /etc/profile.d/draftboard.sh

# dumb-init https://github.com/Yelp/dumb-init
RUN echo "@testing http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories
RUN apk --update add dumb-init@testing

# placing this last as it is a run time variable
ARG DRAFTBOARD_SETTINGS
ENV DJANGO_SETTINGS_MODULE ${DRAFTBOARD_SETTINGS}

# by setting these, we can run `psql` by itself, as well as ref env var in django
# see http://goo.gl/fNG8Do, section `Environment`, for more information
ENV PGHOST postgres
ENV PGUSER postgres
