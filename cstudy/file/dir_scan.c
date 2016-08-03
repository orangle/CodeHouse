/*
扫描某个目录，生成html
*/  
#include<stdio.h>
#include<string.h>
#include<sys/types.h>
#include<dirent.h>

int scan_dir(const char *dir) {
   DIR *dirp; 
   struct dirent *dp;

   if((dirp = opendir(dir)) == NULL) {
        printf("opendir error");
        return 0;
   } else {
        while((dp = readdir(dirp)) != NULL) {
            if (!strcmp(dp->d_name, ".") ||
                    !strcmp(dp->d_name, "..")) {
                continue;
            }
            printf("%s\n", dp->d_name);
        }
        closedir(dirp);
   }
}

int main(void) {

    char *dir = "..";
    scan_dir(dir);
        
    return 0;
}
