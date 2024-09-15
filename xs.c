#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: %s <command>\n", argv[0]);
        return 1;
    }

    char command[256] = "python xsc.py ";
    strcat(command, argv[1]);

    int result = system(command);
    if (result == -1) {
        perror("system() error");
        return 1;
    }

    return 0;
}