ChallName=red-lua
PORT=44191

all:
# make all goes here

compile:
# compile section goes here

run:
# run section goes here

stop:
	docker compose -p ${ChallName} stop
	docker compose -p ${ChallName} rm -f

debug:
	docker compose -p ${ChallName} build
	PORT=${PORT} docker compose -p ${ChallName} up

build:
	docker compose -p ${ChallName} build
	PORT=${PORT} docker compose -p ${ChallName} up -d