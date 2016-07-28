#include<netinet/in.h>
#include<arpa/inet.h>
#include<sys/socket.h>
#include<sys/types.h>
#include<unistd.h>
#include<strings.h>
#include<string.h>
#include<stdio.h>
#include<stdlib.h>

#define MAXLINE 1024
#define PORT 8080

void err_sys(const char *msg){
    perror(msg);
    exit(1);
}

void str_cli(FILE *fp, int sockfd){
   char sendline[MAXLINE], recvline[MAXLINE]; 
   char *rptr;
   int err, n, rn;

   for ( ; ; ){
        rptr = fgets(sendline, MAXLINE, fp);
        if (rptr == NULL) break; 
        n = strlen(sendline);
        err = write(sockfd, sendline, n);
        if (err != n) {
            err_sys("write error");
        }
        bzero(recvline, MAXLINE);
        if ((rn = read(sockfd, recvline, MAXLINE)) <= 0){
            err_sys("read error");
        }

        fputs(recvline, stdout); 
   }
}

int main(int argc, char **argv){
   int i, connfd[5];
   struct sockaddr_in servaddr;

   if (argc != 2){
        err_sys("usage: tcpcli <ipaddress>\n");
   }

   for (i=0; i<5; i++) {
        if((connfd[i] = socket(AF_INET, SOCK_STREAM, 0)) < 0){
           err_sys("socket error\n"); 
        }

        bzero(&servaddr, sizeof(servaddr));
        servaddr.sin_family = AF_INET; 
        servaddr.sin_port = htons(PORT);
        if ((inet_pton(AF_INET, argv[1], &servaddr.sin_addr)) < 1){
            err_sys("pton error");
        }

        if ((connect(connfd[i], (struct sockaddr *)&servaddr, sizeof(servaddr))) < 0){
            err_sys("connect error");
        }
    }

    str_cli(stdin, connfd[0]);
    return 0;
}
