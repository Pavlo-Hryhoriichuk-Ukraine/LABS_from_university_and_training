#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>

void rotate(char *s, int k, bool is_left) {
    int n = strlen(s);
    if (n == 0) return;
    k %= n;
    if (k == 0) return;

    if (!is_left) k = n - k;

    char temp[n + 1];
    strncpy(temp, s + k, n - k);
    strncpy(temp + (n - k), s, k);
    temp[n] = '\0';
    strcpy(s, temp);
}

void shift_chars(char *str, int n, int range) {
    char temp[100] = {0};
    for (int i = 0; str[i] != '\0'; i++)
        temp[i] = (unsigned char)((str[i] + n) % range);
    printf("Resoult (shift chars): %s\n", temp);
}

void rotate_words(char *str, int n, bool is_left) {
    char *words[100];
    int count = 0;

    char *temp_str = strdup(str);
    char *token = strtok(temp_str, " ");
    while (token) {
        words[count++] = strdup(token);
        token = strtok(NULL, " ");
    }

    n %= count;
    char *rotated[100];
    for (int i = 0; i < count; i++) {
        int new_pos = is_left ? (i - n + count) % count : (i + n) % count;
        rotated[new_pos] = words[i];
    }

    str[0] = '\0';
    for (int i = 0; i < count; i++) {
        strcat(str, rotated[i]);
        if (i < count - 1) strcat(str, " ");
        free(rotated[i]);
    }
    free(temp_str);
}


int main() {
    char s[256];
    int n;

    printf("Input string: ");
    fgets(s, 256, stdin);
    s[strcspn(s, "\n")] = 0;

    printf("Rotate characters (n): ");
    scanf("%d", &n);
    rotate(s, n, true);
    printf("Result: %s\n", s);

    printf("Shift char codes (n): ");
    scanf("%d", &n);
    shift_chars(s, n, 256);

    printf("Rotate words (n): ");
    scanf("%d", &n);
    rotate_words(s, n, false);
    printf("Result: %s\n", s);
    return 0;
}