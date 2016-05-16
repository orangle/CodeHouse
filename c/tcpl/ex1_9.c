#include<stdio.h>

//编写一个将输入复制到输出的程序，并将其中连续的多个空格用一个空格代替
//遇到第一个空格，直接复制过去，然后标记取到了空格，下一个会判断前一个字符是否取到了空格

int main(){
    int c, flag;

    flag = 0;

    while ((c=getchar()) != EOF){
        if (c == ' '){
            if (!flag){
                putchar(c);
                flag = 1;
            }
        }else{
           putchar(c); 
           flag = 0;
        }
    }

    return 0;
}
