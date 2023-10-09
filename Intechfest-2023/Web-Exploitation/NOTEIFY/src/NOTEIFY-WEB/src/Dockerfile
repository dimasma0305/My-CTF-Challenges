FROM golang:latest as build
 
EXPOSE 8080

WORKDIR /app
COPY go.mod .
COPY go.sum .
RUN go mod download
COPY . .
RUN CGO_ENABLED=1 go build -o noteify

FROM ubuntu:latest

WORKDIR /app
COPY --from=build /app/noteify .
CMD [ "./noteify" ]