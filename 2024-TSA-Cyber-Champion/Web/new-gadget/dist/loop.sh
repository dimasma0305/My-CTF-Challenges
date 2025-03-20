#!/bin/bash

while true; do
    docker compose down --volumes && docker compose up --build --detach
    sleep 2m
done
