#include<stdio.h>
#define AMOUNT 10000

//这个版本的效率比 binsearch.c 的效率高很多
int binsearch(int x, int v[], int n);

int binsearch(int x, int v[], int n){
    int low = 0, mid;
    int high = n - 1;

    while(low < high) {
       mid = (low + high) / 2;
       if(x <= v[mid]){
            high = mid;
       }else{
            low = mid + 1;
       }
    }
    return (x==v[low]) ? low: -1;
}

int main(){
    int x = 10, n = 10, i;
    int v[10] = {1, 2, 5, 10, 18, 21, 32, 34, 35, 36};
    
    for(i=0; i<AMOUNT; i++){
        int res = binsearch(x, v, n);
        if (res > -1){
            printf("res is %d\n", v[res]);
        }else{
            printf("not found\n"); 
        }
    }
    return 0;
}
