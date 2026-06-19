#include <stdio.h>
#include <math.h>

double get_convex_polygon_area(double (*coords)[2], int n);
void input_coords(double (*coords)[2], int place);
double distance(double x1, double y1, double x2, double y2);
double triangle_area(double a, double b, double c);
double cross(double ax, double ay, double bx, double by, double cx, double cy);
int is_convex_polygon(double (*coords)[2], int n);

int main(void)
{
    int n;
    printf("Enter the number of sides of your convex polygon: ");
    scanf("%d", &n);

    double coords[n][2];

    for (int i = 0; i < n; i++)
    {
        input_coords(coords, i);
        while (!is_convex_polygon(coords, i + 1))
        {
            printf("Invalid input, polygon is not convex, try again!\n");
            input_coords(coords, i);
        }
    }

    printf("Area: %f\n", get_convex_polygon_area(coords, n));
    return 0;
}

void input_coords(double (*coords)[2], int place)
{
    printf("Input X-coord of %d-point: ", place + 1);
    scanf("%lf", &coords[place][0]);
    printf("Input Y-coord of %d-point: ", place + 1);
    scanf("%lf", &coords[place][1]);
}

double distance(double x1, double y1, double x2, double y2)
{
    return sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2));
}

double triangle_area(double a, double b, double c)
{
    double s = (a + b + c) / 2.0;
    return sqrt(s * (s - a) * (s - b) * (s - c));
}

double cross(double ax, double ay, double bx, double by, double cx, double cy)
{
    return (bx - ax) * (cy - by) - (by - ay) * (cx - bx);
}            

int is_convex_polygon(double (*coords)[2], int n)
{
    if (n < 3) return 1;

    int sign = 0;

    for (int i = 0; i < n; i++)
    {
        double ax = coords[i][0],          ay = coords[i][1];
        double bx = coords[(i+1)%n][0],    by = coords[(i+1)%n][1];
        double cx = coords[(i+2)%n][0],    cy = coords[(i+2)%n][1];

        double c = cross(ax, ay, bx, by, cx, cy);

        if (c == 0.0) continue;
        if (sign == 0)
            sign = (c > 0) ? 1 : -1;
        else if ((c > 0 && sign < 0) || (c < 0 && sign > 0))
            return 0;
    }
    return 1;
}

double get_convex_polygon_area(double (*coords)[2], int n)
{
    double sum = 0.0;
    double x0 = coords[0][0], y0 = coords[0][1];

    for (int i = 1; i < n - 1; i++)
    {
        double a = distance(coords[i][0],   coords[i][1],   x0, y0);
        double b = distance(coords[i+1][0], coords[i+1][1], x0, y0);
        double c = distance(coords[i][0],   coords[i][1],   coords[i+1][0], coords[i+1][1]);
        sum += triangle_area(a, b, c);
    }
    return sum;
}