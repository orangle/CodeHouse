#include "apue.h"

int main(int argc, char *argv[]){
   int i;
   struct stat buf;
   char *pstr;

   if (argc < 2){
        printf("usage: %s file1 file2 ..\n", argv[0]);        
   }

   for (i=1; i<argc; i++) {
        printf("%s ", argv[i]);
        
        if (lstat(argv[i], &buf) < 0) {
            printf("lstat error");
            continue;
        }

        if (S_ISREG(buf.st_mode)) {
            pstr = "regluar";
        } else if (S_ISDIR(buf.st_mode)) {
            pstr = "directory";
        } else {
            pstr = "unknow type";
        }
        printf("%s \n", pstr);
   }

   return 0;
}
