/*
atof 字符串转换成浮点型
对atof进行扩充，使它可以处理形如 123.45e-5的数据
*/

#include<stdio.h>
#include<ctype.h>

double atof(char s[]);
int powercal(int base, int exp);

int main(){
    char s[8] = "123.44";
    double b;
    b = atof(s);
    printf("str:%s  double:%f\n", s, b);

    char s2[10] = "56.34e+6";
    b = atof(s2);
    printf("str:%s  double:%f\n", s2, b);

    return 0;
}

//计算平方
int powercal(int base, int exp){
    int res = 1;
    if (exp == 0)
        return 1;
    while (exp-- > 0){
        res *= base; 
    }
    return res;
}

double atof(char s[]){
    int i, sign, esign, exp; 
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

    //处理小数部分
    for (power=1.0; isdigit(s[i]); i++) {
        val = 10.0 * val + (s[i] - '0');
        power = power * 10.0;
    }

    if (s[i] == 'E' || s[i] == 'e') {
        i++;
    }
    if (s[i] == '+' || s[i] == '-') {
        esign = s[i];
        i++;
    }

    //获取指数的值
    for(exp=0; isdigit(s[i]); i++){
        exp = 10.0 * exp + (s[i] - '0');
    }
    
    //printf("val %f\n", val); 
    if (esign == '-') {
        return sign * val / power /  powercal(10, exp); 
    } else {
        return sign * val / power * powercal(10, exp);
    }
}
