#include<stdio.h>
#define MAX 1000

//TCPL 练习4.1

// 获取所有的字符，存到一个数组中
int getline2(char line[], int max);
int strindex(char line[], char t[]);

char p[] = "he";

int getline2(char line[], int max){
   int i = 0; 
   int c;
    
   while(--max>0 && (c = getchar())!=EOF && c !='\n'){
        line[i++] = c;
   }
   line[i] = '\0';
   return i;
}

int strindex(char line[], char t[]){
    int i, j, k;
    int flag = -1;

    for(i=0; line[i]!='\0'; i++){
        for(j=i, k=0; t[k]!='\0'&&line[j]==t[k]; j++, k++){
            ;
        }
        //printf("k %d %c \n", k, t[k-1]); 
        if(k>0 && t[k]=='\0'){
            flag = i;
            break;
        }
    }

    //printf("flag %d", flag);
    if (flag > -1 && line[i+k] == '\0'){
        return flag;
    }

   return -1; 
}

int main(void) {
    char line[MAX]; 
    int z;

    while(getline2(line, MAX) > 0){
        if((z = strindex(line, p)) > -1){
            printf("found:  %s\n", line);
        }
        //printf("%d\n", z);
    }

    return 0;
}


