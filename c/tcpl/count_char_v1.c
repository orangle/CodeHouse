#include<stdio.h>

/* 可以使用 ./a.out < xxx.txt  标准输入来测试*/

int main(){
    int c = 0;
    while (getchar() != EOF){
        ++c;
    }
    printf("%d\n", c);
    return 0;
}
