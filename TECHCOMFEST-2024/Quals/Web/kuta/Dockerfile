FROM python:buster

EXPOSE 80

RUN apt-get -qqy update && \
    apt-get -qqy --no-install-recommends install \
    qutebrowser xvfb cron && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/*
RUN pip install flask

COPY ./flag.txt /flag.txt
RUN mv /flag.txt `cat /proc/sys/kernel/random/uuid`.txt

RUN useradd ctf --create-home
ENV DISPLAY=:99

WORKDIR /app

COPY ./app /app/
RUN echo "#!/bin/sh\nrm -rf /tmp/*" > /cls
RUN crontab -l | { cat; echo "*/30 * * * * /cls"; } | crontab

CMD ["bash","-c","cron & Xvfb :99 -screen 0 640x400x8 -nolisten tcp & runuser -u ctf -- python /app/server.py"]
