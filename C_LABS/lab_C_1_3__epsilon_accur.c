#include <stdio.h>
#include <math.h>

double R_O_W_(int a, double e, long long int *number)
{
    double current = 100.0;
    long int k = 0;
    double a_sqr = (double)(a * a);
    double sum = 0.0;

    while (fabs(current) > e)
    {
        k++;
        if (k % 2 == 0)
            current = pow(k, 0.9) / (a_sqr + pow(k, 2));
        else
            current = (-1 * pow(k, 0.9)) / (a_sqr + pow(k, 2));
        sum += current;
        if (k >= 10000)
            break;
    }
    *number = k; // write a result in adress
    return sum;
}

int main()
{
    double epsilon = 10.00;
    int a = 0;
    
    printf("       ");

    for (int i = 0; i < 10; i++)
    {
        printf("| e=%.1e   ", epsilon);
        epsilon *= 0.1;
    }
    printf("\n\n");
    epsilon = 10.00;

    for (int i_a = 0; i_a < 10; i_a++)
    {
        printf(" a = %d |", a);
        for (int i_e = 0; i_e < 10; i_e++)
        {
            long long int number = 0;
            double result = R_O_W_(a, epsilon, &number);
            printf("% .4f-%5lld|",result, number);
            epsilon *= 0.1;
        }
        epsilon = 10.00;
        a += 1;
        printf("\n");
    }

    return 0;
}