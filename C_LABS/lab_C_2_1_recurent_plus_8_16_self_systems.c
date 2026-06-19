#include <stdio.h>
#include <math.h>

#define A 10
#define B 11
#define C 12
#define D 13
#define E 14
#define F 15

void print_in_a_proper_way(long long int number_to_translate, char system_char)
{
    if (number_to_translate == 0)
        return;
    print_in_a_proper_way(number_to_translate / system_char, system_char);
    
    char resoult = number_to_translate % system_char;
    switch (resoult)
    {
    case A:
        printf("%c", 'A');
        break;
    case B:
        printf("%c", 'B');
        break;
    case C:
        printf("%c", 'C');
        break;
    case D:
        printf("%c", 'D');
        break;
    case E:
        printf("%c", 'E');
        break;
    case F:
        printf("%c", 'F');
        break;
    default:
        printf("%d",resoult);
        break;
    }
}

int main(void)
{
    int n;
    long long int a0 = 1;
    long long int a1 = 2;
    long long int a2;

    printf("Input natural number: ");
    scanf("%d", &n);
    
    if (n == 0)
        a2 = 1;
    else if (n == 1)
        a2 = 2;
    else
        for (int i = 3; i <= n; i++)
        {
            a2 = 4 * a1 - 4 * a0 + i * pow(2, i);
            a0 = a1;
            a1 = a2;
        }
    printf("DECIMAL: %lld", a2);
    printf("\nBIN: ");
    print_in_a_proper_way(a2, 2);
    printf("\nOCT: ");
    print_in_a_proper_way(a2, 8);
    printf("\nHEX: ");
    print_in_a_proper_way(a2, 16);
}