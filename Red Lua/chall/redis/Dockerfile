FROM vulhub/redis:5.0.7

COPY flag.txt /flag.txt

RUN /bin/sh -c set -ex &&\
    apt-get update &&\
    apt-get install -y --no-install-recommends wget ca-certificates &&\
    apt-get install -y --no-install-recommends $(apt-cache depends redis-tools | grep Depends | sed "s/.*ends:\ //" | tr '\n' ' ')

RUN /bin/sh -c set -ex &&\
    cd /tmp &&\
    wget http://archive.ubuntu.com/ubuntu/pool/universe/r/redis/redis-server_5.0.7-2_amd64.deb &&\
    wget http://archive.ubuntu.com/ubuntu/pool/universe/r/redis/redis-tools_5.0.7-2_amd64.deb &&\
    wget http://archive.ubuntu.com/ubuntu/pool/universe/r/redis/redis_5.0.7-2_all.deb &&\
    dpkg -i *.deb

RUN /bin/sh -c set -ex &&\
    sed -i 's/bind 127.0.0.1 ::1/bind 0.0.0.0/g' /etc/redis/redis.conf &&\
    sed -i 's/protected-mode yes/protected-mode no/g' /etc/redis/redis.conf &&\
    sed -i 's/daemonize yes/daemonize no/g' /etc/redis/redis.conf &&\
    sed -i 's|logfile .*|logfile /dev/stdout|g' /etc/redis/redis.conf

USER redis:redis

CMD ["redis-server", "/etc/redis/redis.conf"]
