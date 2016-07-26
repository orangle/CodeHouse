/*
ref:http://space.wccnet.edu/~chasselb/linux275/ClassNotes/web/http.htm
*/   

#include <sys/wait.h> 
#include <sys/socket.h> 
#include <sys/ioctl.h>
#include <netinet/in.h> 
#include <signal.h> 
#include <errno.h>

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
void mysig(int nsig) 
{ 
    int nStatus, nPid; 
    
    if (nsig == SIGCHLD)
        nPid = waitpid(-1, &nStatus, WNOHANG); 
    printf("\nSignal(%d) received\n****************************\n\n\n\n\n\n\n", 
        nsig);    
} 

// **********************************************************
main (int argc, char **argv) 
{ 
    int aPort; 
    char hostname[64];  
    
    if (argc < 2) 
    { 
        fprintf(stderr, 
            "usage:%s porta  \n" , argv[0]); 
        exit(1); 
    } 
    aPort = atoi(argv[1]); 
    gethostname(hostname, sizeof(hostname));
    
    signal(SIGCHLD, mysig); // To clean up terminated children

    // server routine does all of the real work.

    server(hostname, aPort);
    
    exit(0); 
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

void server(char *hostname, int aPort)
{  
    struct sockaddr_in sin, fsin; 
    int fd_connect, fd_accept;   
    int fromlen, nOpt =1; 
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
     
        printf("http: accepting new request\n"); fflush(stdout);
  //
  // process_http handles the new connect request
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
   
    fp = fdopen(fd_http, "r");
    if (fp == NULL)
    {
        fprintf(stderr,"fdopen err : %s\n", strerror(errno));
        return;
    }

// Read the first input line to find out what kind of request we have
 
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
 //
 // The next part is the URL
    
    url = strtok(NULL, " \r\n");
    if (url == NULL)
    {
        fprintf(stderr,"No URL\n");
        return;
    }
    if (url[0] == '/')
        url = &url[1]; // skip over initial /

    fprintf(stderr," url = %s\n", url);
    
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
    
    if (strstr(url, ".cgi") != NULL)
    {
        // CGI_BIN request -- much tougher
        process_cgi(fd_http, fp, request_type, url);
        return;
    }
    
    // Determine what kind of file we have based on suffix.
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
 
void process_cgi(int fd_http, FILE *fp, int request_type, char * url)
{   
    pid_t pid;    
        
    if ((pid = fork()) == 0) 
    { 
       babysit_process(fd_http, fp, request_type, url);
       exit(0);
    } 
    if (pid < 0)
       fprintf(stderr, "**** Can't fork Babysitting Child\n");

    //Main process goes back and waits for a new request
    
}

// **********************************************************
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

// process environment variable stuff
    processEnviron(fp, request_type, url);
 

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
       myChild(request_type, childInput[0], childOutput[1],  url); 
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
    if (fp_output == NULL)
       {
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
     if (strstr(out_buff, "Content-type") == NULL)
     {
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
    execl(prog, (char *)0); 
    fprintf(stderr, "Couldn't execl: %s\n", prog); 
}


// **********************************************************
// The following routine, sets up all of the environment 
// variables for the CGI-BIN program

void processEnviron(FILE *fp,  int request_type, char * url)
{
 
    char *str, *str2;
    char buff[10000];
    char buff2[10000];

    if (request_type == POST_TYPE)
        putenv("REQUEST_METHOD=POST");
    else
    {
        putenv("REQUEST_METHOD=GET");
    
// Split the URL into program name and QUERY_STRING

        str = strchr(url, '?');
        *str = 0; // Null terminate cgi-bin program name
        if (str != NULL)
        {
            sprintf(buff, "QUERY_STRING=\"%s\"", &str[1]);
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
            printf("read http header:%s", str);
            str = strtok(str, " :\r\n");
            str2 = strtok(NULL, " \r\n");
            if (str2 != NULL)
            {
                printf("Header = %s = %s\n", str, str2);
               
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
    printf("Done Processing Headers\n");
}


// **********************************************************
int dir_check(char * url, int fd_http)
{
    return 0; // Not a directory
}
