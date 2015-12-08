#!/usr/bin/env bash

wget -O- https://toolbelt.heroku.com/install.sh | sh
PATH="bin:$PATH"
heroku pg:reset DATABASE_URL






