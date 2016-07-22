#include<stdio.h>

/*
    温度程序的翻转程序 从华氏到摄氏度
    y = x*9/5 + 32
 */

int main(){
    
    float start = -15;
    int end = 150;
    float tmp = 0;

    printf("华氏 摄氏\n");
    while(start < end){
        tmp = start * 9 / 5.0 + 32;
        printf("%3.0f %6.1f\n", start, tmp);
        start += 10;
    }

    return 0;
}

