#!/bin/sh
while true; do
    (docker-compose down --volumes && docker-compose up --build)&
    sleep 60
done
