#include<stdio.h>
#include<arpa/inet.h>

int main(void){
    int port = 8080; 

    //host to net order 解决的是大小端的问题
    printf("8080 htonl Ox%x, htons 0x%x\n", htonl(port), htons(port));

    // ntohs ntohl 网络获取的顺序转回host的
    return 0;
}
