#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>

void print_char_frq(char *s) {
    int freq[256] = {0};
    for (int i = 0; s[i] != '\0' && s[i] != '\n'; i++) 
        freq[(unsigned char)s[i]]++;
        
    for (int i = 0; i < 256; i++) {
        if (freq[i] > 0) printf("'%c': %d\n", i, freq[i]);
    }
}

void print_word_frq(char *s) {
    char *words[100];
    int counts[100] = {0}, unique = 0;
    
    char *copy = strdup(s);
    char *token = strtok(copy, " \t\n");
    
    while (token) {
        bool found = false;
        for (int i = 0; i < unique; i++) {
            if (strcmp(words[i], token) == 0) {
                counts[i]++;
                found = true;
                break;
            }
        }
        if (!found) {
            words[unique] = strdup(token);
            counts[unique] = 1;
            unique++;
        }
        token = strtok(NULL, " \t\n");
    }
    
    for (int i = 0; i < unique; i++) {
        printf("Word: '%s' | Count: %d\n", words[i], counts[i]);
        free(words[i]);
    }
    free(copy);
}

int main() {
    char s[500];
    printf("Input: ");
    fgets(s, sizeof(s), stdin);

    printf("\nChar frequencies:\n");
    print_char_frq(s);

    printf("\nWord frequencies:\n");
    print_word_frq(s);

    return 0;
}