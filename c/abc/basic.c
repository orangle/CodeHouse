/*
author: orangleliu 2014-10-27 
name: basic.c 
*/

#include<stdio.h>

/* Link section */
int total = 0;
int sum(int, int);

int main()
{
    printf("This is a C basic program \n");
    total = sum(1,3);
    printf("Sum of two numbers: %d \n", total);
    getchar();
    return 0;
}

int sum(int a, int b)
{
    return a + b;    
}
