#include <stdio.h>
#include <stdlib.h>

int main()
{
    // Цілі типи та їх розміри
    char a;           // 1 байт: [-128, 127] або [0, 255]
    short int b;      // 2 байти: [-32768, 32767]
    int c;            // 4 байти: [-2147483648, 2147483647]
    long int d;       // 4 або 8 байтів
    long long int e;  // 8 байтів

    unsigned int r;   // 4 байти: від 0 до ~4 млрд
    signed char q;    // 1 байт: явно зі знаком [-128, 127]

    // Дійсні типи
    float k;          // 4 байти
    double h;         // 8 байтів
    long double l;    // 12 або 16 байтів

    // Системи числення
    int dec, hex, oct;
    dec = 100;
    hex = 0x1FA;
    oct = 0144;       // 8-ткова система в C починається з 0

    char ch = 'd';
    printf("ch = %c, code = %d\n", ch, ch);

    /* %c -> символ
       %d, %i -> ціле десяткове
       %u -> unsigned (без знаку)
       %o -> 8-ткова
       %x -> 16-ткова
       %f -> float/double
       %e -> експоненційна форма
       %s -> рядок (string)
    */

    double d1 = 5e-3; // 0.005
    float f1 = 10.0f; // літерал типу float

    size_t size = sizeof(float);
    printf("size of float = %d bytes\n", size);

    printf("Vvedit simvol: ");
    int value1 = getchar(); // читаємо символ
    
    printf("Vi vveli: ");
    putchar(value1);        // виводимо символ
    printf("\n");

    printf("Hello world!\n");

    return 0;
}