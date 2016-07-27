/*
ref:http://space.wccnet.edu/~chasselb/linux275/ClassNotes/web/http.htm
多进程的简单http server
静态文件采用直接处理，cgi请求采用多进程，比较大的篇幅都是cgi的处理

测试使用 hello.cgi
curl  'http://127.0.0.1:8888/Makefile'
curl  'http://127.0.0.1:8888/hello.cgi/?a=b'
curl  'http://127.0.0.1:8888/hello.cgi'
*/

#include <sys/wait.h>
#include <sys/socket.h>
#include <sys/ioctl.h>
#include <netinet/in.h>
#include <signal.h>
#include <errno.h>

#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>

// Prototypes of the modules in this http server

// Main Server code that calls accept
void server(char *hostname, int aPort);

// process_http is called for each http request
void process_http(int fd_http);

// process_cgi is called if the process is a CGI-BIN program
void process_cgi(int fd_http, FILE *fp, int request_type, char * url);

// It is helpful to spawn a separate process to babysit the CGI_BIN prog.
void babysit_process(int fd_http, FILE *fp, int request_type, char * url);

// processEnviron deals with all of the environment variables
void processEnviron(FILE *fp,  int request_type, char * url);

// The actual execution of the CGI-BIN occurs in a spawned process
// that executes myChild
void myChild(int requestType, int fd_in, int fd_out, char * prog);

// This is currently a stub, but is meant to provide
// a web directory listing -- to be done --- student exercise :-)
int dir_check(char * url, int fd_http);


#define good_return "HTTP/1.1 200 OK\r\n"
#define bad_return "HTTP/1.1 500 BAD\r\n Content-Type: text/html\r\n\r\n <html><body><h1>Internal Error</h1></body></html>"
#define notFound_return "HTTP/1.1 404 NotFound\r\n Content-Type: text/html\r\n\r\n <html><body><h1>File Not Found</h1></body></html>"



// **********************************************************
// Signal handler to process terminated children
// SIGCHLD 信号的处理，子进程结束的处理
void mysig(int nsig)
{
    int nStatus, nPid;

    if (nsig == SIGCHLD)
        nPid = waitpid(-1, &nStatus, WNOHANG);
    printf("\nSignal(%d) received ****************************\n",
        nsig);
}

// **********************************************************
// 总的程序入口 获取服务器的地址和端口号 设置信号处理函数
int main (int argc, char **argv)
{
    int aPort;
    char hostname[64];

    // 判断是否输入参数
    if (argc < 2)
    {
        fprintf(stderr,
            "usage:%s porta  \n" , argv[0]);
        exit(1);
    }

    // 获取端口和本机地址
    aPort = atoi(argv[1]);
    gethostname(hostname, sizeof(hostname));

    signal(SIGCHLD, mysig); // To clean up terminated children

    // server routine does all of the real work.

    server(hostname, aPort);

    return 0;
}

// **********************************************************
// Server Loop for processing http Requests
// Any new connect to http results in one of 2 things:
//
// If the request is for a static page (html, htm, gif, jpeg), then
// the appropriate file is loaded and sent.
//
// If the request is a cgi-bin request, then a child is spawned
// to baby sit the connection

// 服务器主循环，用来处理http请求
// 主要完成下面2个事情
// 1 如果 请求的是静态资源 html, htm, gif, jepg等，拿到文件并发送给客户端
// 2 如果 如果是个cgi请求 会产生一个子进程来处理这个连接

void server(char *hostname, int aPort)
{
    struct sockaddr_in sin, fsin;
    socklen_t fromlen;
    int fd_connect, fd_accept;
    int nOpt =1;
    long pid;

    printf("http serving: %s:%d\n", hostname, aPort);

// Create Socket
    if ((fd_accept = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    {
        perror("server: socket()");
        exit(1);
    }

// The following option tells the system to recycle the port
// much quicker when this process is restarted.  Otherwise,
// we would have to use different ports when we bounce the server.

    setsockopt(fd_accept, SOL_SOCKET, SO_REUSEADDR, &nOpt, sizeof(int));

    memset(&sin, 0, sizeof(sin));
    sin.sin_family = AF_INET;
    sin.sin_port = htons(aPort);
    sin.sin_addr.s_addr = htonl(INADDR_ANY);

// Bind the port number to the socket

    if (bind(fd_accept, (struct sockaddr *)&sin, sizeof(sin)) < 0)
    {
        perror("server: bind()");
        exit(1);
    }

// Set up a listen queue of 5 for new connect requests
    if (listen(fd_accept, 5) < 0)
    {
        perror("server: listen()");
        exit(1);
    }

    fromlen = sizeof(fsin);

// Wait for each new connect with the accept call
    for (;;)
    {
        if ((fd_connect = accept(fd_accept, (struct sockaddr *)&fsin, &fromlen)) < 0)
        {
            perror("server:accept()");
            continue; /* hope this is normally due to a child death*/
        }

        printf("http: accepting new request ------------- \n"); fflush(stdout);

        // process_http handles the new connect request
        // 处理新请求
        process_http(fd_connect);

        close(fd_connect);
    }

}


// **********************************************************
#define GET_TYPE 1
#define POST_TYPE 2

void process_http(int fd_http)
{
    FILE *fp;
    char buff[10000];
    char buff2[200];
    pid_t pid;


    int request_type=GET_TYPE;
    char *str, *str2;
    char *url, *content_type;
    int len, nread;
    int fd_to_send;

// It's handy to have a FILE stream to read the request
// 打开请求的文件描述符
    fp = fdopen(fd_http, "r");
    if (fp == NULL)
    {
        fprintf(stderr,"fdopen err : %s\n", strerror(errno));
        return;
    }

// Read the first input line to find out what kind of request we have
// 读取第一行 获取到请求方法 GET or POST
    str = fgets(buff, sizeof(buff), fp);
    if (str == NULL)
    {
        fprintf(stderr,"Can't read first line");
        return;
    }
    fprintf(stderr,"Processing: %s\n", str);

// Read off the GET or POST part
    str = strtok(str, " \r\n");
    fprintf(stderr,"Request Type = %s\n", str);

    if (strcmp(str,"POST") == 0)
        request_type = POST_TYPE;

    if (strcmp(str,"GET") == 0)
        request_type = GET_TYPE;

// The next part is the URL
// 解析url
    url = strtok(NULL, " \r\n");
    if (url == NULL)
    {
        fprintf(stderr,"No URL\n");
        return;
    }
    if (url[0] == '/')
        url = &url[1]; // skip over initial /

    fprintf(stderr,"Request url = %s\n", url);

    // Check to see if URL is a directory ... if so list
    // files in dir

    if (dir_check(url, fd_http))
        return;

    // Need some web server rule on what indicates we have
    // a file versus a CGI-BIN program.
    // On Apache, you can define a CGI-BIN directory and you can
    // define a file extension of .cgi
    // I'm going to say that if the URL contains ".cgi" --> its a
    // a CGI-BIN program, otherwise, its a file
    // .cgi 的请求会当做cgi脚本来处理

    if (strstr(url, ".cgi") != NULL)
    {
        // CGI_BIN request -- much tougher
        process_cgi(fd_http, fp, request_type, url);
        return;
    }

    // Determine what kind of file we have based on suffix.
    // 下面都是静态文件的处理
    len = strlen(url);
    content_type = "text/plain"; // default content-type
    if (strcmp(&url[len-4], ".gif") == 0)
        content_type="image/gif";
    if (strcmp(&url[len-4], ".jpg") == 0)
        content_type="image/jpeg";
    if (strcmp(&url[len-4], ".htm") == 0)
        content_type="text/html";

    if (strcmp(&url[len-5], ".jpeg") == 0)
        content_type="image/jpeg";
    if (strcmp(&url[len-5], ".html") == 0)
        content_type="text/html";

    // Web servers usually have some way to map URLs to filenames
    // We are cheating here and taking the simple route.
    // 只是简单读取url对应当前目录的文件，并没有复杂的映射

    fd_to_send = open(url, O_RDONLY );
    if (fd_to_send < 0)
    {
        fprintf(stderr,"Can't open (%s) : %s\n",
            url, strerror(errno));
        write(fd_http,notFound_return, strlen(notFound_return));
        return;
    }


// Write out the first 2 lines of output
    sprintf(buff2, "%s"
                   "Content-type: %s\r\n\r\n", good_return, content_type);
    write(fd_http, buff2, strlen(buff2));


//Send static file (html, htm, gif, jpeg, etc.)
    while ( (nread = read(fd_to_send, buff, sizeof(buff))) > 0)
    {
        write(fd_http, buff, nread);
    }
    close(fd_to_send);

}


// **********************************************************
// To process a CGI-BIN program we spawn a babysitting task.
// 处理 cgi-bin 的请求
void process_cgi(int fd_http, FILE *fp, int request_type, char * url)
{
    pid_t pid;

    if ((pid = fork()) == 0)
    {
       fprintf(stderr, "fork a child process \n");
       babysit_process(fd_http, fp, request_type, url);
       exit(0);
    }
    if (pid < 0)
       fprintf(stderr, "**** Can't fork Babysitting Child\n");

    //Main process goes back and waits for a new request

}

// **********************************************************
// 子进程中对cgi部分的处理过程
void babysit_process(int fd_http, FILE *fp, int request_type, char * url)
{
    pid_t pid;
    int childInput[2];
    int childOutput[2];
    char post_buff[30000];
    char *out_buff;
    char buff2[100];
    char c, *str;
    int nread, content_length=0;
    int total = 0;
    FILE *fp_output;
    int ioctl_flag = 1;
    char *prog;

    // process environment variable stuff
    // 请求method 设置到环境变量中
    processEnviron(fp, request_type, url);

    fprintf(stderr, "child process start cgi \n");
    if (request_type == POST_TYPE)
    {
        // The following will make the socket non-blocking.  This is
        // necessary when we do a POST request, because we need to read
        // out the characters written into the socket while the socket isn't
        // closed yet.

        if (ioctl(fd_http, FIONBIO, &ioctl_flag) < 0)
            perror("ioctl err");

        if (pipe(childInput))
        {
            fprintf(stderr,"pipe(childInput) err: %s\n", strerror(errno));
            return;
        }
        post_buff[0] = 0;
        content_length = fread(post_buff, 1, sizeof(post_buff), fp);
        if (content_length < 0)
            fprintf(stderr,"fread error on input: %s\n", strerror(errno));

        fprintf(stderr ,"CGI-BIN content lenth is %d\n", content_length);
        sprintf(buff2, "CONTENT_LENGTH=%d", content_length);
        fprintf(stderr,"content_length environment variable: %s\n", buff2);
        putenv(strdup(buff2));
    }

    if (pipe(childOutput))
    {
        fprintf(stderr,"pipe(childOutput) err: %s\n", strerror(errno));
        return;
    }

    if ((pid = fork()) == 0)
    {
       //prase url get .cgi name
        prog = strtok(url, "?");
        if (prog[strlen(prog) - 1] == '/'){
            prog[strlen(prog) - 1] = '\0';
        }
        myChild(request_type, childInput[0], childOutput[1], prog);
        exit(0);
    }
    if (pid < 0)
       fprintf(stderr,"**** Can't fork CGI-BIN CHILD\n");

    if (request_type == POST_TYPE)
    {
        close(childInput[0]);// close read side of childInput
        fprintf(stderr,"Writing out %d bytes:\n%s\n", content_length, post_buff);
        write(childInput[1], post_buff, content_length);
    }

    close(childOutput[1]);// close write side of childOutput
    fp_output = fdopen(childOutput[0], "r");
    if (fp_output == NULL) {
            fprintf(stderr,"Can't read child Output:%s\n", strerror(errno));
    }

    // Assume it worked
    out_buff = post_buff;
    total = strlen(good_return);
    strcpy(out_buff, good_return);

    for (;; )
    {
        nread = read(childOutput[0], &out_buff[total], sizeof(post_buff) - total-1);
        if (nread > 0)
            total += nread;
        else
            {
                if (nread < 0)
                    fprintf(stderr,"read error(%s)\n", strerror(errno));
                break;
            }
     }

     out_buff[total] = 0;
     //CGI 的输出中需要带有这个header，header部分之后需要有 \n
     if (strstr(out_buff, "Content-Type") == NULL)
     {
        fprintf(stderr,"content type is null (%s)\n", strerror(errno));
        write(fd_http, bad_return, strlen(bad_return));
     }
     else
     {
       write(fd_http, out_buff, total);
       if (total >= sizeof(post_buff) -1)
         {
            for (;;)
            {
                nread = read(childOutput[0], out_buff, sizeof(post_buff));
                if (nread <= 0 ) break;
                write(fd_http, out_buff, nread);
            }
         }
     }

    printf("cig handle end....");
    close(childInput[1]); // finally close write side of childInput
    close(childOutput[0]); // finally close read side of childOutput
    close (fd_http);
}


// **********************************************************
// Child process to manager one connect requests reads/writes
// When the connection seems to go away, the child terminates

void myChild(int request_type, int fd_in, int fd_out, char * prog)
{
    if (dup2(fd_out, STDOUT_FILENO) < 0)
    {
        perror("dup2 STDOUT failed");
        fflush(stderr);
        return;
    }
    if (request_type == POST_TYPE)
        if (dup2(fd_in, STDIN_FILENO) < 0)
        {
            fprintf(stderr, "fd_in = %d\n", fd_in);
            perror("dup2 STDIN failed");
            fflush(stderr);
            return;
        }

// Become the CGI-BIN program
    fprintf(stderr, "execl: %s\n", prog);
    execl(prog, (char *)0);
}


// **********************************************************
// The following routine, sets up all of the environment
// variables for the CGI-BIN program

void processEnviron(FILE *fp,  int request_type, char * url)
{

    char *str, *str2, *str3;
    char buff[10000];
    char buff2[10000];

    if (request_type == POST_TYPE)
        putenv("REQUEST_METHOD=POST");
    else
    {
        putenv("REQUEST_METHOD=GET");
// Split the URL into program name and QUERY_STRING

        //printf("process evn url: %s\n", url);
        str3 = strchr(url, '?');
        //printf("str3 %s\n", str3);
        //*str3 = 0; // Null terminate cgi-bin program name
        if (str3 != NULL)
        {
            sprintf(buff, "QUERY_STRING=\"%s\"", str3);
            putenv(strdup(buff));
        }
     }

    putenv("HTTP_COOKIE"); // Remove previous HTTP_COOKIE
    putenv("HTTP_REFERER");// Remove previous HTTP_REFERER

// Read in Headers and process the ones we are interested in
// Until an end of line is encounter --- then exit loop

    do
    {
        str = fgets(buff, sizeof(buff), fp);
        if (str != NULL)
        {
            //printf("read http header:%s", str);
            str = strtok(str, " :\r\n");
            str2 = strtok(NULL, " \r\n");
            if (str2 != NULL)
            {
                printf("Header   %s = %s\n", str, str2);

                if (strcmp(str, "Cookie") == 0)
                    {
                        sprintf(buff2, "%s=%s", "HTTP_COOKIE", str2);
                        putenv(strdup(buff2));
                    }
                if (strcmp(str, "Referer") == 0)
                    {
                        sprintf(buff2, "%s=%s", "HTTP_REFERER", str2);
                        putenv(strdup(buff2));
                    }
                if (strcmp(str, "User-Agent") == 0)
                    {
                        sprintf(buff2, "%s=%s", "HTTP_USER_AGENT", str2);
                        putenv(strdup(buff2));
                    }
            }
        }
    } while (str != NULL);
    printf("Done Processing Headers\n\n");
}

// **********************************************************
int dir_check(char * url, int fd_http)
{
    return 0; // Not a directory
}
