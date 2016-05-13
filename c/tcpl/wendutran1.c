#include<stdio.h>

int main(){
    float start = 0;
    float end = 300;
    float tmp = 0;

    printf("摄氏 华氏\n");
    while(start <= end){
       tmp = (start - 32)* 5 / 9;
       printf("%3.0f %6.1f\n", start, tmp);
       start += 20;
    }

    return 0;
}
