#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define FLAG_FILE "/root/flag.txt"

int main(int argc, char *argv[]) {
    FILE *file = fopen(FLAG_FILE, "r");
    if (!file) {
        perror("Failed to open flag file");
        return 1;
    }

    char flag[256];
    if (fgets(flag, sizeof(flag), file) == NULL) {
        perror("Failed to read flag");
        fclose(file);
        return 1;
    }

    fclose(file);
    printf("%s\n", flag);

    return 0;
}
