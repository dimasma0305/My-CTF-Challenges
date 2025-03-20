# Use OpenJDK 17 as the base image for building
FROM openjdk:17-slim

# Print Java version
RUN java -version

# Install Maven directly from the image
RUN apt update && apt install -y maven binutils --no-install-recommends

# Copy source code and build with Maven
COPY . /usr/src/myapp
WORKDIR /usr/src/myapp/
RUN mvn package

# Set up application directory
ARG APP_DIR=/app
RUN mkdir -p $APP_DIR

# Copy the application JAR to the app directory
RUN cp /usr/src/myapp/target/memento-1.0-SNAPSHOT-jar-with-dependencies.jar $APP_DIR/app.jar

# Copy any additional necessary files
COPY ./flag.txt $APP_DIR/flag.txt

# Expose the port for the application
EXPOSE 8080

# Set the working directory and entry point for running the app
WORKDIR $APP_DIR
ENTRYPOINT ["java", "-jar", "./app.jar"]
