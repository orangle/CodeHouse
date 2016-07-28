#include<stdio.h>
#include<string.h>

int main(void){
    char message[] = "/home/dd.cgi/?name=lzz"; 
    char *word;
    
    word = strtok(message, "?");
    printf("1st word: %s\n", word);

    printf("last char %c\n", word[strlen(word) - 1]);
    if (word[strlen(word) - 1] == '/'){
       word[strlen(word) - 1] = '\0'; 
        printf("new word %s\n", word); 
    }

    char *str;
    char msg[] = "/home/dd.cgi/?name=lzz"; 
    str = strchr(msg, 'n');
    //*str = 0;
    if (str != NULL){
        printf("strch %s\n", str);
    }

    //string cmp
    

    return 0;
}
