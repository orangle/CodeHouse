#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <unistd.h>
#include <strings.h>
#include <stdlib.h>
#include <stdio.h>
#include <errno.h>

#define MAXLINE 1024
/*
 echo 服务器端

 select多路复用
*/

void str_echo(int sockfd);
void err_sys(const char* x);
void sig_child(int signo);

void err_sys(const char* x){
    perror(x);
    exit(1);
}

void str_echo(int sockfd){
    int err;
    size_t n;
    char buf[1024];

    while( (n = read(sockfd, buf, 1024)) > 0){
        err = write(sockfd, buf, n);
        if (err != n)
            err_sys("write client error");
    }
}

void sig_child(int signo){
    pid_t pid;
    int stat;

    while ( (pid = waitpid(-1, &stat, WNOHANG)) > 0)
        printf("child %d terminated\n", pid);

    return;
}

int main(void){
    int i, maxi, maxfd;
    int listenfd, connfd, sockfd;
    int nready, client[FD_SETSIZE];
    ssize_t n;
    char buf[1024];
    socklen_t clilen;
    fd_set rset, allset;
    struct sockaddr_in cliaddr, servaddr;
    int port;
    char ipstr[INET_ADDRSTRLEN];


    if((listenfd = socket(AF_INET, SOCK_STREAM, 0)) < 0){
        err_sys("socket error");
    }

    signal(SIGCHLD, sig_child);

    bzero(&servaddr, sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = htonl(INADDR_ANY);
    servaddr.sin_port = htons(8080);

    if (bind(listenfd, (struct sockaddr *)&servaddr, sizeof(servaddr)) < 0){
        err_sys("bind error");
    }

    if (listen(listenfd, 10) < 0){
        err_sys("listen error");
    }

    //add listenfd to select 
    maxfd = listenfd;
    maxi = -1;

    for(i=0; i<FD_SETSIZE; i++) {
        client[i] = -1; 
    }
    
    FD_ZERO(&allset);
    FD_SET(listenfd, &allset);

    printf("server listend 8080 fd_setsize: %d\n", FD_SETSIZE);

    for ( ; ;){
        rset = allset;        
        nready = select(maxfd+1, &rset, NULL, NULL, NULL);
        printf("ready fd num: %d, maxi:%d, maxfd:%d\n", nready, maxi, maxfd);
       
        //handler listen fd
        if (FD_ISSET(listenfd, &rset)) {
            clilen = sizeof(cliaddr);
            connfd = accept(listenfd, (struct sockaddr *)&cliaddr, &clilen);
            if (connfd < 0){
                err_sys("accept error");
            }

            port = ntohs(cliaddr.sin_port);
            inet_ntop(AF_INET, &cliaddr.sin_addr, ipstr, sizeof(ipstr));
            printf("connect client host: %s port: %d\n", ipstr, port);
            //找到一个空槽来放fd
            for (i=0; i<FD_SETSIZE; i++) {
                if (client[i] < 0) {
                    client[i] = connfd;
                    break;
                }
            }

            if (i == FD_SETSIZE) {
                err_sys("too many clients");
            }

            FD_SET(connfd, &allset);
            if (connfd > maxfd) {
                maxfd = connfd;
            }

            if (i > maxi) {
                maxi = i;
            }

            if (--nready <= 0) {
                continue;
            }
        }

        for (i=0; i<=maxi; i++) {
            if ((sockfd = client[i]) < 0) {
                continue;
            }

            if (FD_ISSET(sockfd, &rset)) {
                if ((n = read(sockfd, buf, MAXLINE)) == 0){
                    close(sockfd);
                    FD_CLR(sockfd, &allset);
                    client[i] = -1;
                    printf("close client fd: %d\n", sockfd);
                } else {
                   printf("read from client -> %s", buf);

                   if(write(sockfd, buf, n) < 0) {
                        err_sys("write error");
                   }
                }

                if (--nready <=0) {
                    continue;
                }
            }
        }
    }
    return 0;
}


