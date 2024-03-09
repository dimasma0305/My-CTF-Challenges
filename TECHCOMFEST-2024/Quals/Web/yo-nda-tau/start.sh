#!/bin/bash

while true; do
    docker compose down --volumes && docker compose up -d
    sleep 240
done
