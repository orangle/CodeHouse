#include<stdio.h>

void swap(int *p1, int *p2){
    printf("*p1 %d, *p2 %d\n", *p1, *p2);
    printf("p1 %p, p2 %p\n", p1, p2);
    int temp;
    temp = *p1;
    *p1 = *p2;
    *p2 = temp;
    printf("after swap\n*p1 %d, *p2 %d\n", *p1, *p2);
    printf("p1 %p, p2 %p\n", p1, p2);

    return ;
}

void main(){
    int a, b;
    int *po_1, *po_2;
    a = 4;
    b = 3;

    po_1 = &a;
    po_2 = &b;
    printf("a %d , &a %p \n", a, &a);
    printf("b %d , &b %p \n", b, &b);
    printf("po_1  %p \n", po_1);
    printf("po_2  %p \n", po_2);
    if(a>b) swap(po_1, po_2);
    printf("a %d  \nb %d\n", a, b);
    printf("*po_1 %d\n*po_2 %d \n", *po_1, *po_2);

    return ;
}
