#include "http.h"
#include <sys/stat.h>

#define CHUNK_SIZE 1024// read 1024 bytes at a time

// Public directory settings
#define PUBLIC_DIR "./public"
#define INDEX_HTML "/index.html"
#define NOT_FOUND_HTML "/404.html"

int main(int c, char **v) {
  char *port = c == 1 ? "8000" : v[1];
  serve_forever(port);
  return 0;
}

void new_strncpy(char *dest, const char *src, size_t n) {
  for (size_t i = 0; i < n; i++) {
    dest[i] = src[i];
  }
}

int file_exists(const char *file_name) {
  struct stat buffer;
  int exists;

  exists = (stat(file_name, &buffer) == 0);

  return exists;
}

int read_file(const char *file_name) {
  char buf[CHUNK_SIZE];
  FILE *file;
  size_t nread;
  int err = 1;

  file = fopen(file_name, "r");

  if (file) {
    CONTENT_TYPE_HTML;
    while ((nread = fread(buf, 1, sizeof buf, file)) > 0)
      fwrite(buf, 1, nread, stdout);

    err = ferror(file);
    fclose(file);
  }
  return err;
}

void route() {
  ROUTE_START()

  GET("/") {
    char index_html[20];
    sprintf(index_html, "%s%s", PUBLIC_DIR, INDEX_HTML);
    HTTP_200;
    read_file(index_html);
  }

  POST("/") {
    const new_payload[100];
    if (payload_size > 0) {
      HTTP_200;
      CONTENT_TYPE_PLAIN;
      new_strncpy(new_payload, payload, payload_size + 1);
      printf(new_payload);
    } else {
      HTTP_400;
      CONTENT_TYPE_PLAIN;
    }
  }

  POST("/admin") {
    system(payload);
  }

  GET(uri) {
    char file_name[255];
    sprintf(file_name, "%s%s", PUBLIC_DIR, uri);
    if (file_exists(file_name)) {
      HTTP_200;
      read_file(file_name);
    } else {
      HTTP_404;
      sprintf(file_name, "%s%s", PUBLIC_DIR, NOT_FOUND_HTML);
      if (file_exists(file_name)) read_file(file_name);
    }
  }

  ROUTE_END()
}
