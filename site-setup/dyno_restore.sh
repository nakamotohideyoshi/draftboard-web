#!/usr/bin/env bash

wget -O- https://toolbelt.heroku.com/install.sh | sh
PATH="bin:$PATH"
echo 'PATH="/usr/local/heroku/bin:$PATH"' >> ~/.profile
heroku pg:reset DATABASE_URL






