#include<stdio.h>

int main()
{
    int c, b, t, n;
    b = 0;
    t = 0;
    n = 0;

    while((c=getchar()) != EOF)
    {
        if (c == ' ')
            ++b;
        else if ( c == '\t')
            ++t;
        else if ( c == '\n')
            ++n;
    }

    printf("blank %d, tab %d, line %d \n", b, t, n);
}
