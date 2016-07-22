#include<stdio.h>

void main(){
    int a[] = {1,3,4,5};
    int *pa;
    pa = a;
    printf("*pa = %d \n", *pa);
    printf("*(pa+1) = %d \n", *(pa+1));

    int *p = (int*)10;
}
