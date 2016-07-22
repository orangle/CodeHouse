#include<stdio.h>

/* 简单的统计行数,单词数目，字符个数等*/

int main()
{
    int c, nl, nw, nc, flag;
    nl = nw = nc =0;

    while((c = getchar()) != EOF)
    {
       ++nc;
       if( c == '\n' )
           ++nl;

       if( c == ' '|| c == '\t' || c == '\n')
            flag = 1;
       else if ( flag == 1){
            ++nw;
            flag = 0;
       }
    }

    printf("line %d words %d chars %d \n", nl, nw, nc);
}
