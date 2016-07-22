//判断一个字符串中是否有重复的字符

#include <iostream>
#include <string>
#include <bitset>

using namespace std;

bool isUnique(string input){
    bitset<256> hashMap;
    for(int i=0; i<input.length(); i++){
        if (hashMap[(int)input[i]]){
            return false;
        }
        hashMap[(int)input[i]] = 1;
    }
    return true;
}

int main(){
    string str1 = "abcedefopl";
    string str2 = "abcdefg";

    cout << str1 << " :" << isUnique(str1) << endl;
    cout << str2 << " :" << isUnique(str2) << endl;
    return 0;
}
