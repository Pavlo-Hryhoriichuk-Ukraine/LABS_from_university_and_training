#include <stdio.h>
#include <math.h>
#include <time.h>
#include <stdlib.h>

#define R 10
#define X_0 5
#define Y_0 3
#define K 2
#define B 6

#define X_MIN (X_0 - R)
#define X_MAX (X_0 + R)
#define Y_MIN (Y_0 - R)
#define Y_MAX (Y_0 + R)
#define SQ_AREA ((2 * R) * (2 * R))

#define TERM_B (K * (K * (B - Y_0) - X_0))
#define TERM_A (1 + (K * K))
#define TERM_C (X_0*X_0 + (B-Y_0)*(B-Y_0) - R*R)
#define DISCRIMINANT ((TERM_B * TERM_B) - (4 * TERM_A * TERM_C))

#define PRINT_0_TOUCH printf("A line does not intersect a circle.\n");
#define PRINT_1_TOUCH printf("A line intersects a circle in 1 point.\n");
#define SQ(N, p) printf("The square of " #N " part, " #N " = %d is S%d = %.2lf\n", p, p, s[p])

#if DISCRIMINANT > 0
    #define TWO
#elif DISCRIMINANT == 0
    #define ONE
#else
    #define ZERO
#endif

double s[3] = {0, 0, 0};

void calc_square(void) {
    srand(time(NULL));
    int n_up = 0, n_down = 0;
    const int iterations = 1000000;

    for (int i = 0; i < iterations; i++) {
        double px = X_MIN + ((double)rand() / RAND_MAX) * (X_MAX - X_MIN);
        double py = Y_MIN + ((double)rand() / RAND_MAX) * (Y_MAX - Y_MIN);

        double dx = px - X_0;
        double dy = py - Y_0;
        if (dx * dx + dy * dy <= R * R) {
            if (py > K * px + B) {
                n_up++;
            } else {
                n_down++;
            }
        }
    }

    s[1] = (double)SQ_AREA * ((double)n_up / iterations);
    s[2] = (double)SQ_AREA * ((double)n_down / iterations);
}

int main(void) {
    int k = 2;

    #ifdef TWO
        calc_square();
        SQ(k, k);
    #elif defined(ONE)
        PRINT_1_TOUCH
    #else
        PRINT_0_TOUCH
    #endif

    return 0;
}