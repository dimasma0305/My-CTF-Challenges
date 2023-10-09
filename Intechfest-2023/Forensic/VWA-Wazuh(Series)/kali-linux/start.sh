#!/bin/sh

echo "Waiting 1 minutes ..."
python3 -m http.server 8080 -d /static/ &
sleep 1m
echo "Attacker machine started ..."

while true
do
    find /exploit/ -type f -exec {} \;
    sleep 5m
done
