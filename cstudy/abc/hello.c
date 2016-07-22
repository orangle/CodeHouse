#include<stdio.h>

int main(){
    printf("Hello C \n");    
    
    int age = 12;
    printf("orangleliu age is %d \n", age);

    char a = 'c';
    printf("char size %ld \n", sizeof('a')); //os look at it as int
    printf("char size %ld \n", sizeof(a));
    printf("int size %ld \n", sizeof(2));
    printf("long size %ld \n", sizeof(2L));
    printf("long long size %ld \n", sizeof(2LL));
    printf("float size %ld \n", sizeof(3.44f));
    printf("double size %ld \n", sizeof(5.33));
    
    enum weekday {sun, mon, tue, wed, thu, fri, sat};
    enum weekday b, c;
    c = sun;
    b = mon;
    printf("sun is %d, mon is %d \n", c, b);

    return 0;
}
