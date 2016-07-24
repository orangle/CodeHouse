/*
   1-10
   编写一个将输入复制到输出的程序，并将其中的制表符替换为\t,把回退符
   替换为\b, 把反斜杠替换为 \\. 这样可以将制表符和回退符以可见的方式
   显示出来

   主要考察的是转义字符
*/

#include<stdio.h>

int main(){
    char c; 
        
    while ((c = getchar()) != EOF) {
        if(c == '\t'){
            printf("\\t");
        } else if (c == '\b') {
            printf("\\b");
        } else if (c == '/') {
            printf("\\\\");
        } else {
            printf("%c", c);
        }
    }

   return 0;
}



