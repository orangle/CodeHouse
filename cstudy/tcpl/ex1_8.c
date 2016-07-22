#include<stdio.h>

int main(){
    int c, nl, tl, bl;
    
    nl = 0;
    tl = 0;
    bl = 0;

    while ((c = getchar()) != EOF){
        if (c == ' '){
            ++bl;
        }else if(c == '\t'){
            ++tl;
        }else if(c == '\n'){
            ++nl;
        }
    }

    printf("blank is %d, tab is %d, line is %d\n", bl, tl, nl);

    return 0;
}
