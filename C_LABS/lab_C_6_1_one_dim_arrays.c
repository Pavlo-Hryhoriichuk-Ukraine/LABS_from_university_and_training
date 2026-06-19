#include <stdio.h>
#include <stdlib.h>
#include <windows.h>

int* input_array(int *size)
{
    printf("Input size of your integer array: ");
    scanf("%d", size);
    int* array = malloc(*size * sizeof(int));
    if (array == NULL) return NULL;

    for (int i = 0; i < *size; i++)
    {
        printf("Input %d-element of array: ", i + 1);
        scanf("%d", &array[i]);
    }
    return array;
}

void sort_1_dim_array(int* array, int size)
{
    for (int i = 0; i < size - 1; i++)
    {
        int min_index = i; 
        for (int j = i + 1; j < size; j++)
        {
            if (array[min_index] < array[j])
            {
                min_index = j;
            }
        }
        int temp = array[i];
        array[i] = array[min_index];
        array[min_index] = temp;
    }
}

void print_union_of_2_arrays(int* array_1, int size_1, int* array_2, int size_2)
{
    printf("1-> ");
    int new_size = size_1 + size_2;
    int *new_array = malloc(new_size * sizeof(int));
    if (new_array == NULL) return;

    for (int i = 0; i < size_1; i++)
    {
        new_array[i] = array_1[i];
    }
    for (int i = size_1, j = 0; i < new_size; i++, j++)
    {
        new_array[i] = array_2[j];
    }

    sort_1_dim_array(new_array, new_size);
    for (int i = 0; i < new_size; i++)
    {
        printf("%d ", new_array[i]);
    }
    printf("\n");
    free(new_array);
}

int find_elem(int* array_1, int size_1, int elem)
{
    for (int j = 0; j < size_1; j++) 
    {
        if (array_1[j] == elem) return 1;
    }
    return 0;
}

void print_unique_union_of_2_arrays(int* array_1, int size_1, int* array_2, int size_2)
{
    printf("2-> ");
    int new_size = size_1;
    int *new_array = malloc(new_size * sizeof(int));
    if (new_array == NULL) return;

    for (int i = 0; i < size_1; i++)
    {
        new_array[i] = array_1[i];
    }

    for (int j = 0; j < size_2; j++)
    {
        if (!find_elem(new_array, new_size, array_2[j]))
        {
            int* try_array = realloc(new_array, (new_size + 1) * sizeof(int));
            if (try_array == NULL) 
            {
                free(new_array);
                return;
            }
            new_array = try_array;
            new_array[new_size] = array_2[j];
            new_size++;
        }
    }

    sort_1_dim_array(new_array, new_size);
    for (int i = 0; i < new_size; i++)
    {
        printf("%d ", new_array[i]);
    }
    printf("\n");
    free(new_array);
}

void print_unique_intersection_of_2_arrays(int* array_1, int size_1, int* array_2, int size_2)
{
    printf("3-> ");
    int count = 0;
    int *new_array = NULL;

    for (int j = 0; j < size_2; j++)
    {
        if (find_elem(array_1, size_1, array_2[j]) && !find_elem(new_array, count, array_2[j]))
        {
            int* try_array = realloc(new_array, (count + 1) * sizeof(int));
            if (try_array == NULL) 
            {
                free(new_array);
                return;
            }
            new_array = try_array;
            new_array[count] = array_2[j];
            count++;
        }
    }

    if (count > 0) 
    {
        sort_1_dim_array(new_array, count);
        for (int i = 0; i < count; i++)
        {
            printf("%d ", new_array[i]);
        }
    } 
    else 
    {
        printf("Empty array of intersection");
    }
    free(new_array);
    printf("\n");
}

int main(void)
{   
    int size_1, size_2;
    int *array_1 = input_array(&size_1);
    int *array_2 = input_array(&size_2);

    if (array_1 == NULL || array_2 == NULL) 
    {
        free(array_1);
        free(array_2);
        return 1;
    }

    print_union_of_2_arrays(array_1, size_1, array_2, size_2);
    print_unique_union_of_2_arrays(array_1, size_1, array_2, size_2);
    print_unique_intersection_of_2_arrays(array_1, size_1, array_2, size_2);

    free(array_1); 
    free(array_2);
    return 0;
}