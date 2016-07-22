/* 
author: orangleliu 2014-10-27
name: printtest.c
*/

#include<stdio.h>

int main()
{
    char ch = 'A';
    char str[20] = "fresh2refresh.com" ;
    float flt = 10.33 ;
    int no = 150 ;
    double dbl = 20.333434 ;
    char ch1;
    char str1[100];
    
    printf("Character is %c \n", ch) ;
    printf("String is %s \n", str) ;
    printf("Float value is %f \n", flt) ;
    printf("Int value is %d \n", no) ;
    printf("Double value is %lf \n", dbl) ;
    printf("Ocatl value is %o \n", no) ;
    printf("Hex value is %x \n", no) ;
    
    printf("\n");
    
    printf("Enter any character \n");
    scanf("%c", &ch1);
    printf("Enter character is %c \n", ch1);
    printf("Enter any string (upto 100 character) \n");
    scanf("%s", &str1);
    printf("Enter string is %s \n", str1);
    
  
    getchar();
    return 0;
}
