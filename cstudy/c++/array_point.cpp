#include<iostream>
using namespace std;

#define MAX 3 

int main(){
    int arr[MAX] = {10, 11, 12};  
    int *p = NULL;

    p = arr; //这个给地址跟int char不一样
    for(int i=0; i<MAX; i++) {
        cout << "addr: "<< p << " value: " << *p <<endl;
        p++;
    }

    p--;
    for(int i=0; i<MAX; i++){
        cout << "add: " << p << " value:" << *p << endl;
        p--;
    }
    
//    return 0;
}

