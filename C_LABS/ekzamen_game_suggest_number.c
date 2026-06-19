#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(void) {
    srand(time(NULL));
    int number = rand() % 1000;
    char first_digit = number / 100;
    char second_digit = (number / 10) % 10;
    char third_digit = number % 10;
    int suggested_number;

    for (int counter = 0; ; counter++)
    {
        printf("Input your suggestion: ");
        scanf("%d", &suggested_number);
        char sug_first_digit = suggested_number / 100;
        char sug_second_digit = (suggested_number / 10) % 10;
        char sug_third_digit = suggested_number % 10;

        if (suggested_number == number)
        {
            printf("You won (number of tries: %d) !!!\n", counter);
            break;
        }

        if (sug_first_digit == first_digit)
            printf("FIRST DIGIT -> Congrats: %d is in the right place, coutinue!\n", sug_first_digit);
        else if (sug_first_digit == second_digit || sug_first_digit == third_digit)
            printf("FIRST DIGIT -> Good: %d is in the number, but the place is wrong.\n", sug_first_digit);
        
        if (sug_second_digit == second_digit)
            printf("SECOND DIGIT -> Congrats: %d is in the right place, coutinue!\n", sug_second_digit);
        else if (sug_second_digit == third_digit || sug_second_digit == first_digit)
            printf("SECOND DIGIT -> Good: %d is in the number, but the place is wrong.\n", sug_second_digit);
        
        if (sug_third_digit == third_digit)
            printf("THIRD DIGIT -> Congrats: %d is in the right place, coutinue!\n", sug_third_digit);
        else if (sug_third_digit == second_digit || sug_third_digit == first_digit)
            printf("THIRD DIGIT -> Good: %d is in the number, but the place is wrong.\n", sug_third_digit);
    }
    
    return 0;
}