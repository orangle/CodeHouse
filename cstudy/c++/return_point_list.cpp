//返回数组指针
#include <iostream>
#include <ctime>
using namespace std;

int * getRandom(){
    //必须声明为static
    static int r[10];

    srand((unsigned)time(NULL));
    for(int i=0; i<10; i++){
        r[i] = rand();
    }
    return r;
}

int main(){
    int *p;
    p = getRandom();

    for(int i=0; i<10; i++){
        cout << i << ":" << *(p+i) << endl; 
    }
    
    return 0;
}




