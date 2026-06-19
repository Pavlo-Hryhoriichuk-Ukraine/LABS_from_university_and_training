#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX 500

void rm_symbols(char *s1, char *s2) {
    int i, j = 0;
    for (i = 0; s1[i] != '\0'; i++) {
        if (!strchr(s2, s1[i])) {
            s1[j++] = s1[i];
        }
    }
    s1[j] = '\0';
}

char* mix_strings(char* s1, char* s2) {
    char *res = malloc(MAX);
    res[0] = '\0';
    char *copy1 = strdup(s1), *copy2 = strdup(s2);
    char *t1 = strtok(copy1, " "), *t2 = strtok(copy2, " ");

    while (t1 || t2) {
        if (t2) { strcat(res, t2); strcat(res, " "); t2 = strtok(NULL, " "); }
        if (t1) { strcat(res, t1); strcat(res, " "); t1 = strtok(NULL, " "); }
    }
    free(copy1); free(copy2);
    return res;
}

void normalize(char *w) {
    int j = 0;
    for (int i = 0; w[i]; i++) if (isalnum(w[i])) w[j++] = tolower(w[i]);
    w[j] = '\0';
}

void find_sim_words(char *s1, char *s2) {
    char *c1 = strdup(s1), *c2 = strdup(s2);
    char *t1 = strtok(c1, " ");
    while (t1) {
        normalize(t1);
        if (*t1) {
            char *c2_tmp = strdup(c2);
            char *t2 = strtok(c2_tmp, " ");
            while (t2) {
                normalize(t2);
                if (strcmp(t1, t2) == 0) { printf("Common: %s\n", t1); break; }
                t2 = strtok(NULL, " ");
            }
            free(c2_tmp);
        }
        t1 = strtok(NULL, " ");
    }
    free(c1); free(c2);
}

int main() {
    char s1[MAX], s2[MAX];
    printf("Str 1: "); fgets(s1, MAX, stdin); s1[strcspn(s1, "\n")] = 0;
    printf("Str 2: "); fgets(s2, MAX, stdin); s2[strcspn(s2, "\n")] = 0;

    rm_symbols(s1, s2);
    printf("Result 'rm symbols': %s\n", s1);

    char *m = mix_strings("Hello world", "One two");
    printf("Result 'mix_strings': %s\n", m); free(m);

    printf("Result 'find_sym_words': \n");
    find_sim_words("Apple, apple!", "apple orange");

    return 0;
}