#include <stdio.h>
#include <math.h>

#define H 7
#define W 5

#define ZERO 0
#define ONE 1
#define TWO 2
#define THREE 3
#define FOUR 4
#define FIVE 5
#define SIX 6
#define SEVEN 7
#define EIGHT 8
#define NINE 9

    char Zero[H][W] = {
    {' ', ' ', '*', ' ', ' '},
    {' ', '*', ' ', '*', ' '},
    {' ', '*', ' ', '*', ' '},
    {' ', '*', ' ', '*', ' '},
    {' ', '*', ' ', '*', ' '},
    {' ', '*', ' ', '*', ' '},
    {' ', ' ', '*', ' ', ' '}
};

char One[H][W] = {
    {' ', ' ', '*', ' ', ' '},
    {' ', '*', '*', ' ', ' '},
    {'*', ' ', '*', ' ', ' '},
    {' ', ' ', '*', ' ', ' '},
    {' ', ' ', '*', ' ', ' '},
    {' ', ' ', '*', ' ', ' '},
    {'*', '*', '*', '*', '*'}
};

char Two[H][W] = {
    {' ', ' ', '*', '*', ' '},
    {' ', '*', ' ', '*', ' '},
    {' ', ' ', ' ', '*', ' '},
    {' ', '*', '*', '*', ' '},
    {' ', '*', ' ', ' ', ' '},
    {' ', '*', ' ', ' ', ' '},
    {' ', '*', '*', '*', ' '}
};

char Three[H][W] = {
    {' ', ' ', '*', '*', ' '},
    {' ', '*', ' ', '*', ' '},
    {' ', ' ', ' ', '*', ' '},
    {' ', ' ', '*', '*', ' '},
    {' ', ' ', '*', ' ', ' '},
    {' ', ' ', ' ', '*', ' '},
    {' ', '*', '*', '*', ' '}
};

char Four[H][W] = {
    {' ', '*', ' ', '*', ' '},
    {' ', '*', ' ', '*', ' '},
    {' ', '*', ' ', '*', ' '},
    {' ', '*', '*', '*', ' '},
    {' ', ' ', ' ', '*', ' '},
    {' ', ' ', ' ', '*', ' '},
    {' ', ' ', ' ', '*', ' '}
};

char Five[H][W] = {
    {'*', '*', '*', '*', '*'},
    {'*', ' ', ' ', ' ', ' '},
    {'*', ' ', ' ', ' ', ' '},
    {'*', '*', '*', '*', '*'},
    {' ', ' ', ' ', ' ', '*'},
    {' ', ' ', ' ', ' ', '*'},
    {'*', '*', '*', '*', '*'}
};

char Six[H][W] = {
    {'*', '*', '*', '*', '*'},
    {'*', ' ', ' ', ' ', ' '},
    {'*', ' ', ' ', ' ', ' '},
    {'*', '*', '*', '*', '*'},
    {'*', ' ', ' ', ' ', '*'},
    {'*', ' ', ' ', ' ', '*'},
    {'*', '*', '*', '*', '*'}
};

char Seven[H][W] = {
    {'*', '*', '*', '*', '*'},
    {' ', ' ', ' ', ' ', '*'},
    {' ', ' ', ' ', '*', ' '},
    {' ', ' ', '*', ' ', ' '},
    {' ', ' ', '*', ' ', ' '},
    {' ', ' ', '*', ' ', ' '},
    {' ', ' ', '*', ' ', ' '}
};

char Eight[H][W] = {
    {' ', '*', '*', '*', ' '},
    {'*', ' ', ' ', ' ', '*'},
    {'*', ' ', ' ', ' ', '*'},
    {' ', '*', '*', '*', ' '},
    {'*', ' ', ' ', ' ', '*'},
    {'*', ' ', ' ', ' ', '*'},
    {' ', '*', '*', '*', ' '}
};

char Nine[H][W] = {
    {'*', '*', '*', '*', '*'},
    {'*', ' ', ' ', ' ', '*'},
    {'*', ' ', ' ', ' ', '*'},
    {'*', '*', '*', '*', '*'},
    {' ', ' ', ' ', ' ', '*'},
    {' ', ' ', ' ', ' ', '*'},
    {'*', '*', '*', '*', '*'}
};

int main(void)
{
    printf("Input a number: ");
    long long int number;
    scanf("%lld", &number);
    long long int copy_number = number;
    int lenght = 0;

    if (copy_number == 0) lenght = 1;

    while (copy_number > 0) {
        copy_number /= 10;
        lenght++;
    }

    for (int j = 0; j < H; j++)
    {
        for (int i = 1; i <= lenght; i++)
        {
            int digit = (number / (int)(pow(10, (lenght - i)))) % 10;

            switch (digit)
            {
            case ZERO:
            {
                for (int u = 0; u < W; u++) { printf("%c", Zero[j][u]); };
                break;
            }
            case ONE:
            {
                for (int u = 0; u < W; u++) { printf("%c", One[j][u]); };
                break;
            }
            case TWO:
            {
                for (int u = 0; u < W; u++) { printf("%c", Two[j][u]); };
                break;
            }
            case THREE:
            {
                for (int u = 0; u < W; u++) { printf("%c", Three[j][u]); };
                break;
            }
            case FOUR:
            {
                for (int u = 0; u < W; u++) { printf("%c", Four[j][u]); };
                break;
            }
            case FIVE:
            {
                for (int u = 0; u < W; u++) { printf("%c", Five[j][u]); };
                break;
            }
            case SIX:
            {
                for (int u = 0; u < W; u++) { printf("%c", Six[j][u]); };
                break;
            }
            case SEVEN:
            {
                for (int u = 0; u < W; u++) { printf("%c", Seven[j][u]); };
                break;
            }
            case EIGHT:
            {
                for (int u = 0; u < W; u++) { printf("%c", Eight[j][u]); };
                break;
            }
            case NINE:
            {
                for (int u = 0; u < W; u++) { printf("%c", Nine[j][u]); };
                break;
            }
            default:
                break;
            }
        }
        printf("\n");
    }
}