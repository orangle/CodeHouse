#include<iostream>

using namespace std;

int main(){
   int var1;
   char var2[10];

   cout << "var1 address: " << &var1 << endl;
   cout << "var2 address: " << &var2 << endl;

   int num = 10;
   int *p;

   p = &num;

   cout << "p address: " << p << endl;
   cout << "p value: " << *p << endl;
   return 0;
}
