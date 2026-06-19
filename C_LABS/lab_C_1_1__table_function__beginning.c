#include <stdio.h>
#include <math.h>

double func(double x, double y)
{
    return sin(x + y) * pow((pow(x, 3) + pow(y, 1.0/ 3.0)), 1.0 / 2.0) /
    (cos(x - y) + pow((pow(y, 5) + pow(x, 6)), 1.0 / 3.0));
}

int main()
{
    double x_1, x_2, krok_x;
    double y_1, y_2, krok_y;

    printf("Input X:start-end;step: ");
    scanf("%lf-%lf;%lf", &x_1, &x_2, &krok_x);
    printf("Input Y:start-end;step: ");
    scanf("%lf-%lf;%lf", &y_1, &y_2, &krok_y);

int n_x = (int)((x_2 - x_1) / krok_x) + 1;
int n_y = (int)((y_2 - y_1) / krok_y) + 1; // тут + 1 через відрізання хвоста float типом int
int total_num = n_x * n_y;
int half_num = (total_num + 1) / 2; // тут + 1 через те, що нам треба саме кількість точок а не проміжків

printf("    x   |   y   |   f(x,y)|    x   |    y   |   f(x,y)|\n");
printf("#------------------------------------------------------\n");

for (int i = 0; i < half_num; i++)
{
    int i_x = i / n_y; // current number of x
    int i_y = i % n_y; // current number of y

    double current_x_1 = x_1 + i_x * krok_x;
    double current_y_1 = y_1 + i_y * krok_y;

    printf("  %.2f  |  %.2f  |  %.2f  |", current_x_1, current_y_1, func(current_x_1, current_y_1));

    int j = i + half_num; 
    if (j < total_num)
    {
        int j_x = j / n_y;
        int j_y = j % n_y;

        double current_x_2 = x_1 + j_x * krok_x;
        double current_y_2 = y_1 + j_y * krok_y;

        printf("  %.2f  |  %.2f  |  %.2f  |", current_x_2, current_y_2, func(current_x_2, current_y_2));
    }

    printf("\n");
    printf("#------------------------------------------------------\n");
}
    return 0;
}