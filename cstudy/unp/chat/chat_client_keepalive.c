/*
聊天程序中增加心跳机制，固定时间自动检测和重连tcp

全局一个有效的socket fd，三个线程

读
一个线程专门用来读取socket的数据

写
一个线程用来接收键盘的事件，写信息到服务端
一个线程用来保活，在连接空闲的时候定时发送心跳


应用层心跳为什么要有？
1 因为 TCP KeepAlive 是用于检测连接的死活，而心跳机制则附带一个额外的功能：检测通讯双方的存活状态. 例如服务端业务层无法响应，但是tcp keepalive 却是可以正常检测。
2 如果有socks代理，keepalive就无法使用了
3 协议切换的成本低，例如从tcp切换到udp

心跳设计的思路：多久应答？重试几次才确认？timer的开始结束时间？

测试程序
客户端  无心跳， 有心跳keepalive, 有心跳（应用层）
服务端  无要求，支持或者不支持应用层心跳应答都可以

http://biancheng.dnbcw.info/linux/366100.html
https://hengyunabc.github.io/why-we-need-heartbeat/
http://www.cnblogs.com/my_life/articles/4045696.html
https://www.felix021.com/blog/read.php?2076
http://www.tldp.org/HOWTO/html_single/TCP-Keepalive-HOWTO/ 原理

在一些比较简单的情况下，KeepAlive 也开始可以使用的。
keepalive心跳配置

int keepAlive = 1;   // 开启keepalive属性. 缺省值: 0(关闭)
int keepIdle = 60;   // 如果在60秒内没有任何数据交互,则进行探测. 缺省值:7200(s)
int keepInterval = 5;   // 探测时发探测包的时间间隔为5秒. 缺省值:75(s)
int keepCount = 2;   // 探测重试的次数. 全部超时则认定连接失效..缺省值:9(次)
setsockopt(s, SOL_SOCKET, SO_KEEPALIVE, (void*)&keepAlive, sizeof(keepAlive));
setsockopt(s, SOL_TCP, TCP_KEEPIDLE, (void*)&keepIdle, sizeof(keepIdle));
setsockopt(s, SOL_TCP, TCP_KEEPINTVL, (void*)&keepInterval, sizeof(keepInterval));
setsockopt(s, SOL_TCP, TCP_KEEPCNT, (void*)&keepCount, sizeof(keepCount));

这是linux的宏定义 <netinet/tcp.h>
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

#include <netdb.h>
#include <unistd.h>
#include <pthread.h>

#include <arpa/inet.h>
#include <netinet/in.h>
#include <netinet/tcp.h>
#include <sys/types.h>
#include <sys/socket.h>

#define SERVERIP "192.168.59.3"
#define SERVERPORT 8080

#define BUFFSIZE 1024
#define ALIASLEN 32
#define OPTLEN 16
#define LINEBUFF 2048

struct PACKET {
    char option[OPTLEN]; // instruction
    char alias[ALIASLEN]; // client's alias
    char buff[BUFFSIZE]; // payload
};

struct USER {
        int sockfd; // user's socket descriptor
        char alias[ALIASLEN]; // user's name
};

struct THREADINFO {
    pthread_t thread_ID; // thread's pointer
    int sockfd; // socket file descriptor
};

int isconnected, sockfd;
char option[LINEBUFF];
struct USER me;

int connect_with_server();
void setalias(struct USER *me);
void logout(struct USER *me);
void login(struct USER *me);
void *receiver(void *param);
void sendtoall(struct USER *me, char *msg);
void sendtoalias(struct USER *me, char * target, char *msg);

int main(int argc, char **argv) {
    int sockfd, aliaslen;

    memset(&me, 0, sizeof(struct USER));

    while(gets(option)) {
        if(!strncmp(option, "exit", 4)) {
            logout(&me);
            break;
        }
        if(!strncmp(option, "help", 4)) {
            FILE *fin = fopen("help.txt", "r");
            if(fin != NULL) {
                while(fgets(option, LINEBUFF-1, fin)) puts(option);
                fclose(fin);
            }
            else {
                fprintf(stderr, "Help file not found...\n");
            }
        }
        else if(!strncmp(option, "login", 5)) {
            char *ptr = strtok(option, " ");
            ptr = strtok(0, " ");
            memset(me.alias, 0, sizeof(char) * ALIASLEN);
            if(ptr != NULL) {
                aliaslen =  strlen(ptr);
                if(aliaslen > ALIASLEN) ptr[ALIASLEN] = 0;
                strcpy(me.alias, ptr);
            }
            else {
                strcpy(me.alias, "Anonymous");
            }
            login(&me);
        }
        else if(!strncmp(option, "alias", 5)) {
            char *ptr = strtok(option, " ");
            ptr = strtok(0, " ");
            memset(me.alias, 0, sizeof(char) * ALIASLEN);
            if(ptr != NULL) {
                aliaslen =  strlen(ptr);
                if(aliaslen > ALIASLEN) ptr[ALIASLEN] = 0;
                strcpy(me.alias, ptr);
                setalias(&me);
            }
        }
        else if(!strncmp(option, "sendto", 5)) {
            char *ptr = strtok(option, " ");
            char temp[ALIASLEN];
            ptr = strtok(0, " ");
            memset(temp, 0, sizeof(char) * ALIASLEN);
            if(ptr != NULL) {
                aliaslen =  strlen(ptr);
                if(aliaslen > ALIASLEN) ptr[ALIASLEN] = 0;
                strcpy(temp, ptr);
                while(*ptr) ptr++; ptr++;
                while(*ptr <= ' ') ptr++;
                sendtoalias(&me, temp, ptr);
            }
        }
        else if(!strncmp(option, "send", 4)) {
            sendtoall(&me, &option[5]);
        }
        else if(!strncmp(option, "logout", 6)) {
            logout(&me);
        }
        else fprintf(stderr, "Unknown option...\n");
    }
    return 0;
}

void login(struct USER *me) {
    int recvd;
    if(isconnected) {
        fprintf(stderr, "You are already connected to server at %s:%d\n", SERVERIP, SERVERPORT);
        return;
    }
    sockfd = connect_with_server();
    if(sockfd >= 0) {
        isconnected = 1;
        me->sockfd = sockfd;
        if(strcmp(me->alias, "Anonymous")) setalias(me);
        printf("Logged in as %s\n", me->alias);
        printf("Receiver started [%d]...\n", sockfd);
        struct THREADINFO threadinfo;
        pthread_create(&threadinfo.thread_ID, NULL, receiver, (void *)&threadinfo);

    }
    else {
        fprintf(stderr, "Connection rejected...\n");
    }
}

int connect_with_server() {
    int newfd, err_ret;
    struct sockaddr_in serv_addr;
    struct hostent *to;

    /* generate address */
    if((to = gethostbyname(SERVERIP))==NULL) {
        err_ret = errno;
        fprintf(stderr, "gethostbyname() error...%d\n", err_ret);
        return -1;
    }

    /* open a socket */
    if((newfd = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
        err_ret = errno;
        fprintf(stderr, "socket() error... %d\n", err_ret);
        return -1;
    }

    /* set initial values */
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(SERVERPORT);
    serv_addr.sin_addr = *((struct in_addr *)to->h_addr);
    memset(&(serv_addr.sin_zero), 0, 8);

	int keepAlive = 1;   // 开启keepalive属性. 缺省值: 0(关闭)
	int keepIdle = 60;   // 如果在60秒内没有任何数据交互,则进行探测. 缺省值:7200(s)
	int keepInterval = 10;   // 探测时发探测包的时间间隔为5秒. 缺省值:75(s)
	int keepCount = 2;   // 探测重试的次数. 全部超时则认定连接失效..缺省值:9(次)
	setsockopt(newfd, SOL_SOCKET, SO_KEEPALIVE, (void*)&keepAlive, sizeof(keepAlive));
	setsockopt(newfd, SOL_TCP, TCP_KEEPIDLE, (void*)&keepIdle, sizeof(keepIdle));
	setsockopt(newfd, SOL_TCP, TCP_KEEPINTVL, (void*)&keepInterval, sizeof(keepInterval));
	setsockopt(newfd, SOL_TCP, TCP_KEEPCNT, (void*)&keepCount, sizeof(keepCount));

    /* try to connect with server */
    if(connect(newfd, (struct sockaddr *)&serv_addr, sizeof(struct sockaddr)) == -1) {
        err_ret = errno;
        fprintf(stderr, "connect() error... err_ret:%d \n", err_ret);
        //why not close fd
        close(newfd);
        return -1;
    }
    else {
        printf("Connected to server at %s:%d\n", SERVERIP, SERVERPORT);
        return newfd;
    }
}

void logout(struct USER *me) {
    int sent;
    struct PACKET packet;

    if(!isconnected) {
        fprintf(stderr, "You are not connected...\n");
        return;
    }

    memset(&packet, 0, sizeof(struct PACKET));
    strcpy(packet.option, "exit");
    strcpy(packet.alias, me->alias);

    /* send request to close this connetion */
    sent = send(sockfd, (void *)&packet, sizeof(struct PACKET), 0);
    isconnected = 0;
}

void setalias(struct USER *me) {
    int sent;
    struct PACKET packet;

    if(!isconnected) {
        fprintf(stderr, "You are not connected...\n");
        return;
    }

    memset(&packet, 0, sizeof(struct PACKET));
    strcpy(packet.option, "alias");
    strcpy(packet.alias, me->alias);

    /* send request to close this connetion */
    sent = send(sockfd, (void *)&packet, sizeof(struct PACKET), 0);
}

void *receiver(void *param) {
    int recvd;
    struct PACKET packet;

    printf("Waiting here [%d]...\n", sockfd);
    while(isconnected) {

        recvd = recv(sockfd, (void *)&packet, sizeof(struct PACKET), 0);
        if(!recvd) {
        	//接收线程获取socket关闭状态
            fprintf(stderr, "Connection lost from server...\n");
            isconnected = 0;
            close(sockfd);
            break;
        }
        if(recvd > 0) {
            printf("[%s]: %s\n", packet.alias, packet.buff);
        }
        memset(&packet, 0, sizeof(struct PACKET));
    }
    return NULL;
}

void sendtoall(struct USER *me, char *msg) {
    int sent;
    struct PACKET packet;

    if(!isconnected) {
        fprintf(stderr, "You are not connected...\n");
        return;
    }

    msg[BUFFSIZE] = 0;

    memset(&packet, 0, sizeof(struct PACKET));
    strcpy(packet.option, "send");
    strcpy(packet.alias, me->alias);
    strcpy(packet.buff, msg);

    /* send request to close this connetion */
    sent = send(sockfd, (void *)&packet, sizeof(struct PACKET), 0);

    //send需要封装，自动重新连接和发送
    if(send < 0){
    	printf("send error.. sockfd %d\n", sockfd);
    }
}

void sendtoalias(struct USER *me, char *target, char *msg) {
    int sent, targetlen;
    struct PACKET packet;

    if(target == NULL) {
        return;
    }

    if(msg == NULL) {
        return;
    }

    if(!isconnected) {
        fprintf(stderr, "You are not connected...\n");
        return;
    }
    msg[BUFFSIZE] = 0;
    targetlen = strlen(target);

    memset(&packet, 0, sizeof(struct PACKET));
    strcpy(packet.option, "whisp");
    strcpy(packet.alias, me->alias);
    strcpy(packet.buff, target);
    strcpy(&packet.buff[targetlen], " ");
    strcpy(&packet.buff[targetlen+1], msg);

    /* send request to close this connetion */
    sent = send(sockfd, (void *)&packet, sizeof(struct PACKET), 0);
}

