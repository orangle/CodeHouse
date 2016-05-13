#include<stdio.h>

/* 华氏度 摄氏度 */

int main(){
    
    int s = 0;
    int m = 300;

    for(s = 0; s <= 300; s = s + 20){
        printf("%3d %6.1f\n", s, (5.0/9.0)*(s-32));
    }

    printf("\n\n");
    for(m = 300; m >= 0; m = m -20){
        printf("%3d %6.1f\n", m, (5.0/9.0)*(m-32)); 
    }

    return 0;
}
