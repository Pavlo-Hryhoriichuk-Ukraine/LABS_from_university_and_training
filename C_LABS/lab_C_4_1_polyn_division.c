#include <stdio.h>
#include <stdlib.h>

void show_polynomial(double array[], int size) {
    int degree = size - 1;
    if (size <= 0) { printf("0\n"); return; }

    int first = 1;
    for (int i = 0; i < size; i++) {
        double element = array[i];
        if (element == 0) continue;

        int power = degree - i;
        
        if (!first) printf(element > 0 ? " + " : " - ");
        else if (element < 0) printf("-");
        
        double abs_val = (element < 0) ? -element : element;

        if (abs_val != 1 || power == 0) printf("%.1f", abs_val);

        if (power > 0) {
            printf("x");
            if (power > 1) printf("^%d", power);
        }
        first = 0;
    }
    printf("\n");
}

int main(void) {
    int n1, n2;
    while (1) {
        printf("Length of 1st polynomial (size): ");
        scanf("%d", &n1);
        printf("Length of 2nd polynomial (size): ");
        scanf("%d", &n2);
        if (n1 < n2) {
            printf("Error: 1st must be >= 2nd!\n");
            continue;
        }
        break;
    }

    double *poly1 = malloc(n1 * sizeof(double));
    double *poly2 = malloc(n2 * sizeof(double));
    int q_size = n1 - n2 + 1;
    double *quotient = calloc(q_size, sizeof(double));

    for (int i = 0; i < n1; i++) {
        printf("1st poly element %d: ", i);
        scanf("%lf", &poly1[i]);
    }
    for (int i = 0; i < n2; i++) {
        printf("2nd poly element %d: ", i);
        scanf("%lf", &poly2[i]);
    }

    for (int i = 0; i < q_size; i++) {
        double coeff = poly1[i] / poly2[0];
        quotient[i] = coeff;

        for (int j = 0; j < n2; j++) {
            poly1[i + j] -= coeff * poly2[j];
        }
    }

    printf("\nQuotient: ");
    show_polynomial(quotient, q_size);

    printf("Remainder: ");
    show_polynomial(&poly1[q_size], n2 - 1);

    free(poly1); free(poly2); free(quotient);
    return 0;
}