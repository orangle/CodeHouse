#include<stdio.h>
#define AMOUNT 10000

int binsearch(int x, int v[], int n);

int binsearch(int x, int v[], int n){
    int low = 0;
    int high = n -1;
    int mid;

    while(low <= high){
       mid = (low + high)/2;
       if(x < v[mid]){
            high = mid - 1;
            printf("high %d\n", v[mid]);
       }else if(x > v[mid]){
            low = mid + 1;
            printf("low %d\n", v[mid]);
       }else{
            return mid;
       }
    }
    return -1;
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
