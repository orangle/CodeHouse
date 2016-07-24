/*
atof 字符串转换成浮点型
*/

#include<stdio.h>
#include<ctype.h>

double atof(char s[]);

int main(){
    char s[8] = "123.44";
    double b;
    b = atof(s);
    printf("%f\n", b);
    //printf("%d\n", b);
    return 0;
}

double atof(char s[]){
    int i, sign; 
    double val, power;

    for (i = 0; isspace(s[i]); i++){ //字符串前面的空白
       //printf("%c\n", s[i]); 
       ;
    }

    //处理正负号的问题
    sign = (s[i] == '-') ? -1 : 1;
    if (s[i] == '+' || s[i] == '-')
        i++;

    //处理整数部分 
    for (val = 0.0; isdigit(s[i]); i++) {
        val = 10.0 * val + (s[i] - '0'); 
    }

    if (s[i] == '.') {
        i++;
    }

    for (power=1.0; isdigit(s[i]); i++) {
        val = 10.0 * val + (s[i] - '0');
        power = power * 10.0;
    }

    printf("val %f\n", val); 
    return sign * val / power;
}
