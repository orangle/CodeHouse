#include<stdio.h>

int main(){
    int start = 0;
    int end = 300;
    int tmp = 0;

    while(start <= end){
       tmp = (start - 32)* 5 / 9;
       printf("%d %d\n", start, tmp);
       start += 20;
    }

    return 0;
}
