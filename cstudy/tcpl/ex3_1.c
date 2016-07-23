/*
* Exercise 3-1
 *
 * Our binary search makes two tests inside the loop, when one would
 * suffice (at the price of more tests outside). Write a version with
 * only one test inside the loop and measure the difference in run-time.
*/
#include<stdio.h>
#define AMOUNT 10000

//这个版本的效率比 binsearch.c 的效率高很多
int binsearch(int x, int v[], int n);

int binsearch(int x, int v[], int n){
    int low = 0;
    int high = n - 1;
    int mid = (low+high) / 2;

    while(low <= high && x != v[mid]){
       if(x < v[mid]){
            high = mid - 1;
            //printf("high %d\n", v[mid]);
       }else{
            low = mid + 1;
            //printf("low %d\n", v[mid]);
       }
       mid = (low + high)/2;
    }
    return (x==v[mid]) ? mid: -1;
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
