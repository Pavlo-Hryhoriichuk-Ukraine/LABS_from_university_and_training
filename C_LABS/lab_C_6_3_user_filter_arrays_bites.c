#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <windows.h> 


void func_1__sum_of_bytes(int* array, int size)
{
    for (int i = 0; i < size; i++) {
        int sum = 0;
        unsigned char *byte_ptr = (unsigned char *)&array[i];
        for (int j = 0; j < sizeof(int); j++)
            sum += byte_ptr[j];
        array[i] = sum;
    }
}

void func_2__byte_and_of_2_bytes_of_int(int* array, int size)
{
    for (int i = 0; i < size; i++) {
        unsigned short *byte_ptr = (unsigned short *)&array[i];
        int new_number = byte_ptr[0] & byte_ptr[1];
        array[i] = new_number;
    }
}

int compare_bytes(const void *a, const void *b)
{
    unsigned char arg1 = *(const unsigned char*)a;
    unsigned char arg2 = *(const unsigned char*)b;

    if (arg1 < arg2) return -1;
    if (arg1 > arg2) return 1;
    return 0;
}

void func_3__compare_single_bytes_of_array(int* array, int size)
{
    unsigned char* bytes_ptr = (unsigned char *)array;
    qsort(bytes_ptr, size * sizeof(int), sizeof(unsigned char), compare_bytes);
}

int** main_filter(int number_of_arrays, int** array_of_pointers_to_arrays, int* size_array, void (*filter_func)(int*, int))
{
    int** result_2_dim_array = malloc(number_of_arrays * sizeof(int*));
    
    for (int i = 0; i < number_of_arrays; i++) {
        // глибоке копіювання
        result_2_dim_array[i] = malloc(size_array[i] * sizeof(int));
        for (int j = 0; j < size_array[i]; j++) {
            result_2_dim_array[i][j] = array_of_pointers_to_arrays[i][j];
        }
        
        filter_func(result_2_dim_array[i], size_array[i]);
    }
    return result_2_dim_array;
}

void print_arrays(int n, int** arrays, int* sizes, const char* message)
{
    printf("\n--- %s ---\n", message);
    for (int i = 0; i < n; i++) {
        printf("Масив %d: ", i + 1);
        for (int j = 0; j < sizes[i]; j++) {
            printf("%d", arrays[i][j]);
        }
        printf("\n");
    }
}

int main(void)
{
    SetConsoleOutputCP(65001);
    SetConsoleCP(65001);
    srand(time(NULL));
    int n, k;
    void (*func_array[3])(int*, int) = {func_1__sum_of_bytes, func_2__byte_and_of_2_bytes_of_int, func_3__compare_single_bytes_of_array};
    
    printf("Input number of random arrays: ");
    scanf("%d", &n);
    
    int size_array[n];
    int** array_of_pointers_to_arrays = malloc(n * sizeof(int*));

    for (int i = 0; i < n; i++) {
        printf("Input size of [%d] array: ", i + 1);
        scanf("%d", &size_array[i]);
        array_of_pointers_to_arrays[i] = malloc(size_array[i] * sizeof(int));

        for (int j = 0; j < size_array[i]; j++)
            array_of_pointers_to_arrays[i][j] = rand();
    }

    print_arrays(n, array_of_pointers_to_arrays, size_array, "Початкові масиви");

    printf("\nChoose operation for your arrays [0: Sum, 1: AND halves, 2: Sort bytes]: ");
    scanf("%d", &k);
    
    int** result_arrays = main_filter(n, array_of_pointers_to_arrays, size_array, func_array[k]);
    
    print_arrays(n, result_arrays, size_array, "Corrected arrays");

    for (int i = 0; i < n; i++) {
        free(array_of_pointers_to_arrays[i]);
        free(result_arrays[i]);
    }
    free(array_of_pointers_to_arrays);
    free(result_arrays);

    return 0;
}