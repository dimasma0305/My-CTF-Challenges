FROM openjdk:11

USER www-data
WORKDIR /app

USER root
COPY ./src/build/libs/blog-0.0.1-SNAPSHOT.jar /bin/blog.jar
COPY ./flag.txt .
RUN mv ./flag.txt /`cat /proc/sys/kernel/random/uuid`.txt

USER www-data
EXPOSE 8080
CMD java -jar /bin/blog.jar
