#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <windows.h>

#define GET(array, i, j, cols) array[(i) * (cols) + (j)]

void print_matrix(int* matrix, int rows, int cols)
{
    if (matrix == NULL) return;
    for (int i = 0; i < rows; i++)
    {
        for (int j = 0; j < cols; j++)
        {
            printf("%4d ", GET(matrix, i, j, cols));
        }
        printf("\n");
    }
}

int* input_two_dim_array(int *rows, int *cols)
{
    printf("Введіть кількість рядків: ");
    scanf("%d", rows);
    printf("Введіть кількість стовпців: ");
    scanf("%d", cols);
    
    int* array = malloc((*rows) * (*cols) * sizeof(int));
    if (array == NULL) return NULL;

    for (int i = 0; i < *rows; i++)
    {
        for (int j = 0; j < *cols; j++)
        {
            printf("Елемент [%d][%d]: ", i, j);
            scanf("%d", &GET(array, i, j, *cols));
        }
    }
    return array;
}

int max_elem_and_other_finder(int* array, int rows, int cols, int* neg_count, double* avrg_value)
{
    int size = rows * cols;
    int max_value = array[0]; 
    int total_sum = 0;
    *neg_count = 0; 

    for (int i = 0; i < size; i++)
    {
        int value = array[i]; 
        if (value > max_value) max_value = value;
        if (value < 0) (*neg_count)++;
        total_sum += value;
    }
    
    *avrg_value = (double)total_sum / size; 
    return max_value;
}

int* mult_matrix(int* matrix_1, int rows_1, int cols_1, int* matrix_2, int rows_2, int cols_2)
{
    if (cols_1 != rows_2) return NULL;
    
    int* result_matrix = malloc(rows_1 * cols_2 * sizeof(int));
    if (result_matrix == NULL) return NULL;

    for (int i = 0; i < rows_1; i++)
    {
        for (int j = 0; j < cols_2; j++)
        {
            int total_elem = 0;
            for (int p = 0; p < cols_1; p++) 
            {
                total_elem += GET(matrix_1, i, p, cols_1) * GET(matrix_2, p, j, cols_2);
            }
            GET(result_matrix, i, j, cols_2) = total_elem;
        }
    }
    return result_matrix;
}

bool is_magic_square(int* array, int rows, int cols)
{
    if (rows != cols) return false; 
    
    int n = rows;
    int magic_const = (n * ((n * n) + 1)) / 2;
    int diag1_sum = 0, diag2_sum = 0;

    for (int i = 0; i < n; i++)
    {
        diag1_sum += GET(array, i, i, n);
        diag2_sum += GET(array, i, n - 1 - i, n);
        
        int row_sum = 0, col_sum = 0;
        for (int j = 0; j < n; j++)
        {
            row_sum += GET(array, i, j, n);
            col_sum += GET(array, j, i, n); 
        }
        
        if (row_sum != magic_const || col_sum != magic_const) return false;
    }
    
    if (diag1_sum != magic_const || diag2_sum != magic_const) return false;

    return true;
}

int main()
{
    SetConsoleOutputCP(65001);
    SetConsoleCP(65001);
    int r1, c1, r2, c2;
    
    printf("\n=== ІНІЦІАЛІЗАЦІЯ ПЕРШОЇ МАТРИЦІ ===\n");
    int* array_1 = input_two_dim_array(&r1, &c1);
    
    if (array_1 != NULL) {
        printf("\nВаша перша матриця:\n");
        print_matrix(array_1, r1, c1);
        
        int neg_count = 0;
        double avrg = 0.0;
        int max = max_elem_and_other_finder(array_1, r1, c1, &neg_count, &avrg);
        printf("\n[Аналіз матриці 1]\nМаксимум: %d\nСереднє: %.2f\nК-сть від'ємних: %d\n", max, avrg, neg_count);
        
        if (is_magic_square(array_1, r1, c1)) {
            printf("Ця матриця Є магічним квадратом!\n");
        } else {
            printf("Ця матриця НЕ є магічним квадратом.\n");
        }
    }

    printf("\n=== ІНІЦІАЛІЗАЦІЯ ДРУГОЇ МАТРИЦІ ===\n");
    int* array_2 = input_two_dim_array(&r2, &c2);
    
    if (array_2 != NULL) {
        printf("\nВаша друга матриця:\n");
        print_matrix(array_2, r2, c2);
    }

    if (array_1 != NULL && array_2 != NULL) {
        printf("\n=== РЕЗУЛЬТАТ МНОЖЕННЯ МАТРИЦЬ ===\n");
        int* multiplied = mult_matrix(array_1, r1, c1, array_2, r2, c2);
        
        if (multiplied != NULL) {
            print_matrix(multiplied, r1, c2);
            free(multiplied);
        } else {
            printf("Помилка множення: Кількість стовпців 1-ї матриці не дорівнює кількості рядків 2-ї!\n");
        }
    }

    if (array_1 != NULL) free(array_1);
    if (array_2 != NULL) free(array_2);

    printf("\nПрограму успішно завершено.\n");
    return 0;
}