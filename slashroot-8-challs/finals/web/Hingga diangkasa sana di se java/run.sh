#!/bin/bash

while true; do
    docker compose down --volumes && docker compose up --build --detach
    sleep 5m
done
