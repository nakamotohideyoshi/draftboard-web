FROM mendsley/alpine-redis

# use our custom conf
COPY redis.conf /usr/local/etc/redis/redis.conf

# override command to include custom conf
CMD [ "redis-server", "/usr/local/etc/redis/redis.conf" ]
