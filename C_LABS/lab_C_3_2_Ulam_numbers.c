#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    int n;
    printf("Input n-number: ");
    scanf("%d", &n);

    int *seq = calloc(n, sizeof(int));
    if (seq == NULL)
    {
        printf("Memory problem");
        return -1;
    }

    seq[0] = 1;
    seq[1] = 2;
    int count = 2;

    int candidate = 3;
    while (count < n)
    {
        int ways = 0;
        for (int i = 0; i < count && ways < 2; i++)
            for (int j = i + 1; j < count && ways < 2; j++)
                if (seq[i] + seq[j] == candidate)
                    ways++;

        if (ways == 1)
            seq[count++] = candidate;

        candidate++;
    }

    printf("Ulam's [%d] number is %d\n", n, seq[n - 1]);
    
    free(seq);
    return 0;
}