FROM ubuntu:23.04
WORKDIR /app
COPY ./target/release/notewebsite /bin/app
RUN chmod +x /bin/app
COPY ./view ./view
EXPOSE 8080
CMD [ "app" ]
