#include <stdio.h>

int main() {
    FILE *file;
    char ch;
    const char *filename = "/root/flag.txt";
    file = fopen(filename, "r");
    if (file == NULL) {
        printf("Error opening the file.\n");
        return 1;
    }
    printf("Flag contents:\n");
    while ((ch = fgetc(file)) != EOF) {
        putchar(ch);
    }
    fclose(file);
    return 0;
}
