#include <stdio.h>
void repeat_(int k, char symbol)
{
    for (int i = 1; i <= k; i++)
        printf("%c", symbol);
}

int main(void) 
{
    int n, tab, diff;
    int stars = 1;
    printf("Input n-number for your house volume: ");
    scanf("%d", &n);
    int stars_rep = (n > 7) ? 2 : 1;
    diff = (stars_rep % 2 ==0) ? 6 : 4;

    repeat_(n-2, ' ');
    repeat_(1 ,'*');
    printf("\n");

    for (int i = 1; i <= n / 2; i++)
    {   
        tab = n-i-2;
        stars += 2;
        repeat_(tab, ' ');
        repeat_(stars, '*');
        printf("\n");
    }

    for (int i = 0; i < n / 3; i++)
    {
        printf("%*s", tab + 1, " ");
        repeat_(stars_rep, '*');

        repeat_(stars - diff, ' ');
        repeat_(stars_rep, '*');
        printf("\n");
    }
    repeat_(tab + 1, ' ');
    repeat_(stars - 2, '*');
    return 0;
}