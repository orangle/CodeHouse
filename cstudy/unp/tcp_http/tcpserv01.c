#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <unistd.h>
#include <strings.h>
#include <stdlib.h>
#include <stdio.h>
#include <errno.h>

/*
 echo 服务器端
 采用多进程的架构

 子进程的退出没有处理，资源无法释放
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
    int listenfd, connfd;
    pid_t childpid;
    socklen_t clilen;
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

    for ( ; ;){
        clilen = sizeof(cliaddr);
        connfd = accept(listenfd, (struct sockaddr *)&cliaddr, &clilen);
        if (connfd < 0){
            err_sys("accept error");
        }

        port = ntohs(cliaddr.sin_port);
        inet_ntop(AF_INET, &cliaddr.sin_addr, ipstr, sizeof(ipstr));

        if( (childpid = fork()) == 0) {

            close(listenfd);
            str_echo(connfd);
            exit(0);
        }
        printf("connect client host: %s port: %d\n", ipstr, port);
        close(connfd);
    }

    return 0;
}


