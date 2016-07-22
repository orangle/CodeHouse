#include<unistd.h>
#include<stdlib.h>

int main(){
    if ((write(1, "Here is some date\n", 18)) != 18){
        write(2, "some error happended\n",20);   
    }
    exit(0);
}
