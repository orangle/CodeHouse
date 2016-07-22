//变量的范围
#include <iostream>
using namespace std;

int g;

int main(){
    int a, b;
    int c;

    a = 10;
    b = 20;
    c = a + b;

    cout << c <<endl;
    g = 100;
    cout << g << endl;

    return 0;
}
