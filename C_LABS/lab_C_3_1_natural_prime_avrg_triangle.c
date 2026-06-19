#include <stdio.h>
#include <math.h>
#include <stdbool.h>

#define M_PI 3.14159265358979323846

bool _1_input_natural(int *n)
{
    printf("Input n-number: ");
    scanf("%d", n);
    
    if (*n < 1)
    {
        printf("Inputted number is incorrect!");
        return false;
    }
    return true;
}

bool _2_is_prime_number(int number)
{
    for (int i = 2; (double)i <= sqrt(number); i++) // чи добре тут ? (побітові?, приведення?)
        if (number % i == 0)
            return false;
    return true;
}

double _3_avrg_arithmetic_smaller_nums(int number)
{
    long long int sum = 0;
    int count = 0;
    for (int i = 2; i < number; i++)
        if (_2_is_prime_number(i))
        {
            sum += i;
            count++;
        }
    if (count == 0) return 0;
    return (double)sum / count;
}

double _4_avrg_geometric_smaller_nums(int n)
{
    double log_sum = 0;
    int count = 0;
    for (int i = 2; i < n; i++)
        if (_2_is_prime_number(i)) { log_sum += log((double)i); count++; } // добре так чи зле ?
    if (count == 0) return 0;
    return exp(log_sum / count);
}

double _5_avrg_harmonic_smaller_nums(int number)
{
    double sp_sum = 0;
    int count = 0;
    for (int i = 2; i < number; i++)
        if (_2_is_prime_number(i))
        {
            sp_sum += 1.0/i;
            count++;
        }
    return count / sp_sum;
}

void _6_triangle_type(int a, int b, int c)
{
    if (a + b <= c || a + c <= b || b + c <= a)
    {
        printf("Triangle with sides [%d,%d,%d] can not be created", a, b, c);
        return;
    }

    double A = acos((double)(b*b + c*c - a*a) / (2.0*b*c));
    double B = acos((double)(a*a + c*c - b*b) / (2.0*a*c));
    double C = acos((double)(a*a + b*b - c*c) / (2.0*a*b));

    double max_angle = fmax(A, fmax(B, C));

    double Ad = A * 180.0 / M_PI;
    double Bd = B * 180.0 / M_PI;
    double Cd = C * 180.0 / M_PI;

    if (fabs(max_angle - M_PI / 2) < 1e-9)
        printf("Right triangle. Angles: [%.2f; %.2f; %.2f], sides: [%d,%d,%d]", Ad, Bd, Cd, a, b, c);
    else if (max_angle < M_PI / 2)
        printf("Acute triangle. Angles: [%.2f; %.2f; %.2f], sides: [%d,%d,%d]", Ad, Bd, Cd, a, b, c);
    else
        printf("Obtuse triangle. Angles: [%.2f; %.2f; %.2f], sides: [%d,%d,%d]", Ad, Bd, Cd, a, b, c);
}
int main(void)
{
    int n;
    if (_1_input_natural(&n) && _2_is_prime_number(n))
    {
        int a = _3_avrg_arithmetic_smaller_nums(n);
        int b = _4_avrg_geometric_smaller_nums(n);
        int c = _5_avrg_harmonic_smaller_nums(n);

        _6_triangle_type(a, b, c);
    }
    return 0;
}