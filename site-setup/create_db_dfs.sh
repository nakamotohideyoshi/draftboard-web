#!/usr/bin/env bash
sudo -u vagrant createdb dfs
sudo su - postgres
sudo psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE dfs TO vagrant;"
exit
