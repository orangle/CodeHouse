#include<stdio.h>

void main(){
    int x=123;
    int *p = &x;
    printf("x %d \n", x);
    printf("*p %p \n", p);

    int myarr[4] = {0, 1, 2, 4};
    int *pr = myarr;
    printf("pr = %p \n", &*pr);
    printf("*&x = %d \n", *&x);

    return;
}
