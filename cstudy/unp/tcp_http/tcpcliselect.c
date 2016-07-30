#include<netinet/in.h>
#include<arpa/inet.h>
#include<sys/socket.h>
#include<sys/types.h>
#include<sys/select.h>
#include<unistd.h>
#include<strings.h>
#include<string.h>
#include<stdio.h>
#include<stdlib.h>

#define MAXLINE 1024
#define MIN(a,b) (((a)<(b))?(a):(b)))
#define MAX(a,b) (((a)>(b))?(a):(b))

void err_sys(const char *msg){
    perror(msg);
    exit(1);
}

void str_cli(FILE *fp, int sockfd){
    int maxfdp1, stdineof;
    fd_set rset;
    char buf[MAXLINE];
    int n;

    stdineof = 0;
    FD_ZERO(&rset);
    for ( ; ; ) {
        if (stdineof == 0) {
            FD_SET(fileno(fp), &rset); 
        }
        FD_SET(sockfd, &rset);
        // max filedes+1
        maxfdp1 = MAX(fileno(fp), sockfd) + 1;
        if (select(maxfdp1, &rset, NULL, NULL, NULL) < 0) {
            err_sys("select error");
        }

        if (FD_ISSET(sockfd, &rset)) {
            if ((n = read(sockfd, buf, MAXLINE)) == 0) {
                if (stdineof == 1) {
                    return; 
                } else {
                    err_sys("str_cli server stop"); 
                }
            }
            write(fileno(fp), buf, n);
        }

        if (FD_ISSET(fileno(fp), &rset)) {
            if ((n = read(fileno(fp), buf, MAXLINE)) == 0) {
                //stdio eof
                stdineof = 1;
                shutdown(sockfd, SHUT_WR);
                FD_CLR(fileno(fp), &rset);
                continue;
            }
            write(sockfd, buf, n);
        }
    }
}

int main(int argc, char **argv){
    int connfd;
    struct sockaddr_in servaddr;

    if (argc != 2){
        err_sys("usage: tcpcli <ipaddress>\n");
    }

    if((connfd = socket(AF_INET, SOCK_STREAM, 0)) < 0){
       err_sys("socket error\n"); 
    }

    bzero(&servaddr, sizeof(servaddr));
    servaddr.sin_family = AF_INET; 
    servaddr.sin_port = htons(8080);
    if ((inet_pton(AF_INET, argv[1], &servaddr.sin_addr)) < 1){
        err_sys("pton error");
    }

    if ((connect(connfd, (struct sockaddr *)&servaddr, sizeof(servaddr))) < 0){
        err_sys("connect error");
    }

    str_cli(stdin, connfd);
    return 0;
}
