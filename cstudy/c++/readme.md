C++简单的笔记
============

http://www.kancloud.cn/wizardforcel/w3school-cpp/92497

最基本的编译，生产a.out文件
g++ xx.cpp


## 语法相关的
C++ 标识符内不允许出现标点字符，比如 @、$ 和 %，还是大小写字母和下划线

7中基本的数据类型
bool
char
int
float
double
void  无类型
wchar_t 宽字符型

* typeof 类型声明，类似C
* enmu 枚举类型 enmu enum-name {list of names} var-list

全局变量系统会自动初始化，局部变量不会。
常量是字面量

定义常量
1. 使用 `#define`
2. 使用 `const`

修饰符类型
1. signed  字符
2. unsigned 字符
3. long  双精度
4. short

控制语句 循环

```
while(con){
	do somethings;
}

for(init; con; change){
	do somethings;
}

do{
	do somethings;
}while(con)
```

控制语句 条件判断

```
break
continue
goto

Exp1 ? Exp2 : Exp3;

if(con1){

}else{

}

if(con1){

}else if(){

}else{

}

switch(expression){
    case constant-expression  :
       statement(s);
       break; // 可选的
    case constant-expression  :
       statement(s);
       break; // 可选的

    // 您可以有任意数量的 case 语句
    default : // 可选的
       statement(s);
}
```

## 指针

指针初始化为 NULL 是一个好习惯。

指针有算术运算 包括 `++ -- + -` 可以比较大小





