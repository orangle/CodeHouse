/*
url:https://gist.github.com/siritori/3070957


 */

#define _USE_BSD
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <sys/resource.h>
#include <sys/wait.h>
#include <sys/stat.h>
#include <netdb.h>
#include <ctype.h>
#include <string.h>
#include <unistd.h>
#define DOCROOT "./"

struct http_header {
   char *content_type;
   int status;
   size_t length;
};

int    string_split(char *str, const char del, int *countp, char ***vecp);
void   free_string_vector(const int qc, char **vec);
int    strcasecmp(const char *s1, const char *s2);

int    is_valid_request(const char *line, const int argc, char *argv[]);
size_t filesize_of(const char *path);
char*  content_type_of(const char *path);
int    http_server(const int portno);
int    http_receive_request_and_send_reply(int com);
char*  http_receive_request(FILE *in, char *keepalive);
void   http_send_reply(FILE *out, const char *filename);
void   http_reply_header(FILE *out, const struct http_header *header);
void   http_reply_body(FILE *out, FILE *fp, const size_t length);

void   tcp_peeraddr_print(int com);
void   sockaddr_print(const struct sockaddr *addrp, const socklen_t addr_len);

int    tcp_listen_port(const int portno);
void   delete_zombie(void);
int    fdopen_sock(int sock, FILE **inp, FILE **outp);


int main(int argc, char *argv[])
{
   if(argc != 2) {
      fprintf(stdout, "Usage: %s portno\n", argv[0]);
      return 1;
   }
   const int portno = strtol(argv[1], 0, 10);
   if(http_server(portno) == 0) {
      puts("exit on success");
      return 0;
   } else {
      puts("exit on fail");
      return 1;
   }
}

static int countchr(char *s, char c)
{
   int count;
   for(count = 0; *s; ++s) {
      if(*s == c) ++count;
   }
   return count;
}

int string_split(char *str, const char del, int *countp, char ***vecp)
{
   char **vec;
   int count_max, i, len;
   char *s, *p;

   if(str == 0) return -1;
   count_max = countchr(str, del) + 1;
   vec = malloc(sizeof(char *) * (count_max + 1));
   if(vec == NULL) return -1;

   for(i = 0; i < count_max; ++i) {
      while(*str == del) ++str;
      if(*str == 0) break;
      for(p = str; *p != del && *p != 0; ++p) continue;
      len = p - str;
      s = malloc(len + 1);
      if(s == 0) {
         for(int j = 0; j < i; ++j) {
            free(vec[j]);
            vec[j] = 0;
         }
         return -1;
      }
      memcpy(s, str, len);
      s[len] = 0;
      vec[i] = s;
      str = p;
   }
   vec[i] = 0;
   *countp = i;
   *vecp = vec;
   return i;
}

void free_string_vector(const int qc, char **vec)
{
   for(int i = 0; i < qc; ++i) {
      if(vec[i] == NULL) continue;
      free(vec[i]);
   }
   free(vec);
}

int strcasecmp(const char *s1, const char *s2) {
   while(1) {
      while(isspace(*s1)) ++s1;
      while(isspace(*s2)) ++s2;
      if(*s1 == '\0' || *s2 == '\0') break;
      if(tolower(*s1) != tolower(*s2)) return 1;
      ++s1;
      ++s2;
   }
   if(*s1 == '\0' && *s2 == '\0') return 0;
   else return 0;
}

int http_server(const int portno)
{
   const int sock0 = tcp_listen_port(portno);
   if(sock0 < 0) return 1;
   while(1) {
      delete_zombie();
      const int com = accept(sock0, 0, 0);
      fprintf(stderr, "accepts sock:%d\n", com);
      if(com < 0) {
         perror("accept");
         return 1;
      }
      const pid_t child_pid = fork();
      if(child_pid > 0) {
         // parent : continue listen
         close(com);
      } else if(child_pid == 0) {
         // child : communication with client
         close(sock0);
         tcp_peeraddr_print(com);
         return http_receive_request_and_send_reply(com);
      } else {
         perror("fork");
         return 1;
      }
   }
   return 0;
}

#define BUFFERSIZE 1024

int http_receive_request_and_send_reply(const int com)
{
   FILE *in, *out;
   if(fdopen_sock(com, &in, &out) < 0) {
      fprintf(stderr, "fdopen()\n");
      return 1;
   }
   while(1) {
      char keepalive_flag = 0;
      char *filename = http_receive_request(in, &keepalive_flag);

      //const char *home = getenv("HOME");
      const char *home = "";
      const size_t pathlen = strlen(home) + strlen(DOCROOT) + strlen(filename);
      char *path = malloc(pathlen+1);
      if(path == NULL) {
         fprintf(stderr, "FATAL: out of memory\n");
         exit(EXIT_FAILURE);
      }
      if(snprintf(path, pathlen+1, "%s%s%s", home, DOCROOT, filename) < 0) {
         fprintf(stderr, "ERROR: buffer overflow\n");
         http_send_reply(out, NULL);
         free(filename);
      } else {
         http_send_reply(out, path);
         free(filename);
         free(path);
      }
      if(!keepalive_flag) break;
      fprintf(stderr, "[%d] Keep-Alive, continue.\n", getpid());
   }
   fprintf(stderr, "[%d] Keep-Alive done.\n", getpid());
   fclose(in);
   fclose(out);
   return 0;
}

int is_valid_request(const char *line, const int argc, char *argv[]) {
   if(argc != 3) {
      fprintf(stderr, "INVALID REQUEST: invalid number of args\n");
      return 0;
   }
   // check method type
   if(strcmp("GET", argv[0])) {
      fprintf(stderr, "INVALID REQUEST: unrecognized method\n\t%s\n", argv[0]);
      return 0;
   }
   // check file format
   if(argv[1][0] != '/') {
      fprintf(stderr, "INVALID REQUEST: invalid filename\n\t%s\n", argv[1]);
      return 0;
   }
   // check HTTP version
   if(strcmp("HTTP/1.1\r\n", argv[2]) && strcmp("HTTP/1.0\r\n", argv[2])) {
      fprintf(stderr, "INVALID REQUEST: unrecognized version\n\t%s\n", argv[2]);
      return 0;
   }
   // security check
   if(strchr(line, '<') || strstr(line, "..")) {
      fprintf(stderr, "INVALID REQUEST: Dangerous request line\n\t%s\n", line);
      return 0;
   }
   return 1;
}

char* http_receive_request(FILE *in, char *keepalive)
{
   char requestline[BUFFERSIZE];
   fgets(requestline, BUFFERSIZE, in);
   if(ferror(in)) {
      fprintf(stderr, "INVALID REQUEST: No request line.\n");
      return NULL;
   }
   int argc;
   char **argv;
   // split request line
   if(string_split(requestline, ' ', &argc, &argv) < 0) {
      fprintf(stderr, "INVALID REQUEST: failed to split\n\t%s\n", requestline);
      return NULL;
   }
   // request check
   if(!is_valid_request(requestline, argc, argv)) {
      return NULL;
   }
   // default:index.html
   if(argv[1][0] == '/' && argv[1][1] == '\0') {
      free(argv[1]);
      argv[1] = strdup("/index.html");
   }
   char *ret = strdup(argv[1]);
   free_string_vector(argc, argv);
   // read requestline
   *keepalive = 0;
   char rheader[BUFFERSIZE];
   while(fgets(rheader, BUFFERSIZE, in)) {
      if(rheader[0] == '\r' || rheader[0] == '\n') break;
      if(string_split(rheader, ':', &argc, &argv) < 0) {
         fprintf(stderr, "INVALID REQUEST: invalid header format\n");
         return NULL;
      }
      // keep-alive check
      if(!strcasecmp("connection", argv[0]) &&
         !strcasecmp("keep-alive", argv[1])) {
         *keepalive = 1;
      }
      free_string_vector(argc, argv);
   }
   return ret;
}

size_t filesize_of(const char *path)
{
   struct stat s;
   stat(path, &s);
   return s.st_size;
}

char* content_type_of(const char *path)
{
   char *extension = strrchr(path, '.');
   if(extension == NULL || extension[1] == '\0') {
      return "application/octet-stream";
   }
   if(!strcmp(extension, ".txt"))  return "text/plain;charset=utf8";
   if(!strcmp(extension, ".pdf"))  return "application/pdf";;
   if(!strcmp(extension, ".htm"))  return "text/html";
   if(!strcmp(extension, ".html")) return "text/html";
   if(!strcmp(extension, ".css"))  return "text/css";
   if(!strcmp(extension, ".png"))  return "image/png";
   if(!strcmp(extension, ".gif"))  return "image/gif";
   if(!strcmp(extension, ".jpg"))  return "image/jpeg";
   if(!strcmp(extension, ".jpeg")) return "image/jpeg";
   return "application/octet-stream";
}

void http_send_reply(FILE *out, const char *path)
{
   struct http_header header = {
      .status = 400,
      .length = 0,
      .content_type = "text/plain",
   };
   // bad request
   if(path == NULL) {
      http_reply_header(out, &header);
      return;
   }
   fprintf(stderr, "[%d] REQUEST : %s\n", getpid(), path);
   FILE *fp;
   if((fp = fopen(path, "rb")) == NULL) {
      // file not found
      header.status = 404;
      http_reply_header(out, &header);
   } else {
      // file found
      header.status = 200;
      header.length = filesize_of(path);
      header.content_type = content_type_of(path);
      http_reply_header(out, &header);
      http_reply_body(out, fp, header.length);
      fclose(fp);
   }
}

void http_reply_header(FILE *out, const struct http_header *header)
{
   char str[128];
   switch(header->status) {
   case 200:
      sprintf(str, "200 OK");
      break;
   case 404:
      sprintf(str, "404 Not Found");
      break;
   case 400:
      sprintf(str, "400 Bad Request");
      break;
   default:
      // program should not reach here!
      exit(EXIT_FAILURE);
   }
   if(header->status == 200) {
      fprintf(out,
         "HTTP/1.0 %s\r\n"
         "Content-Type: %s\r\n"
         "Content-Length: %d\r\n\r\n",
      str, header->content_type, (int)header->length);
   } else {
       fprintf(out, "HTTP/1.0 %s\r\n\r\n", str);
   }
}

void http_reply_body(FILE *out, FILE *fp, const size_t length)
{
   char *buffer = malloc(length);
   if(fread(buffer, 1, length, fp) < length) {
      fprintf(stderr, "ERROR: failed to read file\n");
      return;
   }
   fwrite(buffer, 1, length, out);
   free(buffer);
   fprintf(stderr, "[%d] data transfer done\n", getpid());
}

void tcp_peeraddr_print(const int com)
{
   struct sockaddr_storage addr;
   socklen_t addr_len  = sizeof(addr);
   if(getpeername(com, (struct sockaddr *) &addr, &addr_len) < 0) {
      perror("tcp_peeraddr_print");
      return;
   }
   fprintf(stderr, "[%d] connect from <", getpid());
   sockaddr_print((struct sockaddr *) &addr, addr_len);
   fprintf(stderr, ">\n");
}

void sockaddr_print(const struct sockaddr *addrp, const socklen_t addr_len)
{
   char host[BUFFERSIZE];
   char port[BUFFERSIZE];
   if(getnameinfo(addrp, addr_len, host, sizeof(host),
                  port, sizeof(port), NI_NUMERICHOST | NI_NUMERICSERV) < 0)
      return;
   fprintf(stderr, "%s:%s", host, port);
}

int tcp_listen_port(const int portno)
{
   const int s = socket(PF_INET, SOCK_STREAM, 0);
   if(s < 0) {
      perror("socket");
      return -1;
   }
   struct sockaddr_in addr = {
      .sin_port        = htons(portno),
      .sin_family      = AF_INET,
      .sin_addr.s_addr = INADDR_ANY,
   };

   if(bind(s, (struct sockaddr *) &addr, sizeof(addr)) < 0) {
      perror("bind");
      fprintf(stderr, "port number %d is already used\n", portno);
      return -1;
   }
   if(listen(s, 5) < 0) {
      perror("listen");
      close(s);
      return -1;
   }
   return s;
}

void delete_zombie()
{
   pid_t pid;
   while((pid = wait4(-1, 0, WNOHANG, 0)) > 0) {
      fprintf(stderr, "[%d] zombi %d deleted.\n", getpid(), pid);
   }
}

int fdopen_sock(int sock, FILE **inp, FILE **outp)
{
   int sock2;
   if((sock2 = dup(sock)) < 0) {
      return -1;
   }
   if((*inp = fdopen(sock2, "r")) == NULL) {
      close(sock2);
      return -1;
   }
   if((*outp = fdopen(sock, "w")) == NULL) {
      fclose(*inp);
      *inp = 0;
      return -1;
   }
   setvbuf(*outp, (char *) NULL, _IONBF, 0);
   return 0;
}
