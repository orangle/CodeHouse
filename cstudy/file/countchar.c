/**
 *输入字符计数
 */

#include<stdio.h>

int main()
{
    long nc, c;
    nc = 0;

    while((c = getchar()) != EOF)
    {
        if (c == '\n')
            ++nc;
    }

    printf("total num is %ld", nc);
}
