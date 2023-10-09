ChallName=go-menasai
PORT=17686

all:
# make all goes here

compile:
# compile section goes here

run:
# run section goes here

stop:
        docker stop ${ChallName}
        docker rm ${ChallName}

debug:
        docker build -t ${ChallName} .
        docker run --restart always --name ${ChallName} -p ${PORT}:8080 -it ${ChallName}

build:
        docker build -t ${ChallName} .
        docker run --restart always --name ${ChallName} -p ${PORT}:8080 -itd ${ChallName}