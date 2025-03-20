#!/bin/sh

CHALL=$(basename "$PWD")
pm2 stop "$CHALL"
pm2 delete "$CHALL"
pm2 start "bash ./loop.sh" --name "$CHALL"
