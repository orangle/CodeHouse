#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>

#include <netinet/tcp.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <netdb.h>

#define MAXBUF 1024
void PANIC(char *msg);
#define PANIC(msg) {perror(msg); abort();} //stdio.h

int http_query(char *host, in_port_t port){
    int sock;  
    int on = 1;
    struct hostent *hp;
    struct sockaddr_in addr;

    if((hp = gethostbyname(host)) == NULL){
        PANIC("get hostname error");
    }

    bcopy(hp->h_addr, &addr.sin_addr, hp->h_length);
    addr.sin_port = htons(port);
    addr.sin_family = AF_INET;
    sock = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP);
    setsockopt(sock, IPPROTO_TCP, TCP_NODELAY, (const char *)&on, sizeof(int));

    if (sock == -1){
        PANIC("set sockopt error"); 
    }

    if(connect(sock, (struct sockaddr *)&addr, sizeof(struct sockaddr_in)) == -1){
        PANIC("connect error");
    }
    

    char buffer[MAXBUF];
    write(sock, "GET /\r\n", strlen("GET /\r\n"));
    bzero(buffer, MAXBUF);

    while(read(sock, buffer, MAXBUF-1) !=0){
        printf("%s", buffer);
        bzero(buffer, MAXBUF);
    }

    shutdown(sock, SHUT_RDWR);
    close(sock);
    printf("http request close");

    return 0;
}


int main(int args, char *argv[]){
    if(args < 3){
        PANIC("Usage: %s <hostname> <port>");
    }

    http_query(argv[1], atoi(argv[2]));
}
