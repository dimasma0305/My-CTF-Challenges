FROM openjdk:11

USER www-data
WORKDIR /app

USER root
COPY ./demo/ /app/

USER www-data
EXPOSE 8080
CMD java -jar build/libs/demo-0.0.1-SNAPSHOT.jar
