#include<stdio.h>
//url http://acm.hdu.edu.cn/showproblem.php?pid=1001

int main(){
    int sum, n, i; 
    while (scanf("%d", &n) != EOF){
        sum = 0;
        for(i=0;i<=n;i++)
            sum = sum + i;
        printf("%d\n\n", sum);
    }
    return 0;
}
