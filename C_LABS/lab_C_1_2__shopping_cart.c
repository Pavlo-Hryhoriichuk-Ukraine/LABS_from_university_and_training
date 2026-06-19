#include <stdio.h>
#include <string.h>

#define ONE 1
#define TWO 2
#define THREE 3
#define FOUR 4
#define FIVE 5

int main()
{
    printf("#----------------------------------------------------------------------------------------#\n");
    printf("Old Spice deodorant \"Bearglove\" 80ml, price: 100hrn, number: 1\n");
    printf("#----------------------------------------------------------------------------------------#\n");
    printf("Mivina \"Kuriacha BIG\" 85g, price: 35hrn , number: 2\n");
    printf("#----------------------------------------------------------------------------------------#\n");
    printf("Oliya Chumak \"Zolotista rafinovana\" 1L, price: 160hrn , number: 3\n");
    printf("#----------------------------------------------------------------------------------------#\n");
    printf("Gillette \"Mack3 turbo\" 5sht., price: 720hrn , number: 4\n");
    printf("#----------------------------------------------------------------------------------------#\n");
    printf("Kniga \"Romko: Yak vigity z Pavlom za odniyeu partou \" 1sht., price: 1000hrn , number: 5\n");
    printf("#----------------------------------------------------------------------------------------#\n");

    printf("\n\nInput data in strict format or 'stop':\n");
    printf("Buy:number of good-how much\n");

    int n1 = 0;
    int n2 = 0;
    int n3 = 0;
    int n4 = 0;
    int n5 = 0;
    int total_price = 0;
    int prod_num;
    int how_much;
     
    while (1) {

        if (scanf(" Buy:%d-%d", &prod_num, &how_much) != 2) { // scanf() повертає кількість підстановок успішних

            printf("Chechout...\n");
            while (getchar() != '\n'); 
            break;
        }
        switch (prod_num)
        {
            case ONE:
                total_price +=  how_much * 100;
                n1 += how_much;
                break;

            case TWO:
                total_price +=  how_much * 35;
                n2 += how_much;
                break;
            
            case THREE:
                total_price +=  how_much * 160;
                n3 += how_much;
                break;
            
            case FOUR:
                total_price +=  how_much * 720;
                n4 += how_much;
                break;
            
            case FIVE:
                total_price +=  how_much * 1000;
                n5 += how_much;
                break;
            default:
                break;
        }
    }
    printf("----------Receipt---------\n");
            if (n1)
                printf("[Old Spice deodorant \"Bearglove\" 80ml], how much: %d\n", n1);
            if (n2)
                printf("[Mivina \"Kuriacha BIG\" 85g], how much: %d\n", n2);
            if (n3)
                printf("[Oliya Chumak \"Zolotista rafinovana\" 1L], how much: %d\n", n3);
            if (n4)
                printf("[Gillette \"Mack3 turbo\" 5sht.], how much: %d\n", n4);
            if (n5)
                printf("[Kniga \"Romko: Yak vigity z Pavlom za odniyeu partou \" 1sht.], how much: %d\n", n5);
    printf("---------------------------------------\n");
    printf("Total price: %d", total_price);

    return 0;
}
