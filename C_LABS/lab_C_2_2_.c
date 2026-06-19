#include <stdio.h>

long long int helper_sum(long long int number, int position)
{
    int sum = 0;
    int pair = 0;
    int i = 1;

    while (number > 0)
{
    int add_num = number % 10;

    if (i >= position)
        pair = 1;

    if ((i + pair) % 2 == 0)
    {
        add_num *= 2;
        if (add_num > 9)
        {
            add_num -= 9;
        }
        sum += add_num;
    }
    else
        sum += add_num;

    number /= 10;
    i++;
}
    printf("%lld\n", sum);
    return sum;
}

int main(void)
{
    long long int number;
    int incomp_sum, lost_digit_pos, mult, to_add;
    long long int incomp_num;
    
    printf("Input your number ");
    scanf("%lld", &number);

    if (helper_sum(number, 100) % 10 == 0)
    printf("Valid number\n");
    else
    printf("Not valid number\n");

    printf("Input incomplete number: ");
    scanf("%lld", &incomp_num);
    printf("Input position of the lost digit: ");
    scanf("%d", &lost_digit_pos);
    incomp_sum = helper_sum(incomp_num, lost_digit_pos);
    
    if (lost_digit_pos % 2 == 0)
    mult = 2;
    else
    mult = 1;

    for (int i = 0; i < 10; i++)
    {   
        to_add = i * mult;
        if (to_add > 9)
        {
            to_add -= 9;
        }

        if ((incomp_sum + to_add) % 10 == 0)
        {
            printf("lost digit: %d", i);
            break;
        }
    }
    return 0;
}