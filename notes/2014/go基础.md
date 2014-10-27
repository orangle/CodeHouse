Go编程基础
=========

#####Go的内置关键字(25个) 不多
break    default    func   interface    select
case     defer      go      map           struct
chan     else        goto   package    switch
const    fallthrough    if    range    type
continute   for     import    return   var

#####Go的注释方法（和js一样）
单行注释： //
多行注释： /**/

#####Go程序一般结构 common_structure.go

* 通过 *package* 组织代码结构（类似python的模块）
* 只有 *package* 名称为 *main* 的包可以包含 *main* 函数
* 一个可执行程序 有且仅有一个 *main* 包
* 通过 *import* 来导入包
* *const* 用来定义常量（类似c）
* 函数体外部使用 *var* 来进行全局变量的声明和赋值
* 复杂类型 *struct* , *interface* 要用 *type* 关键字来声明
* *func* 来声明函数

简单的demo

    /*
    title: common_structure.go
    author: orangleliu
    date: 2014-08-05
    des: the simple demo of erlang
    */

    // a package only have a main
    package main

    // use "import" import other packages
    import "fmt"

    const Lzz = "Orangleliu"

    var name = "erlong"

    type age int

    type golang struct{

    }

    func main(){
        fmt.Println("I love Erlog!")
    }

1 导入多个包的方法

    import (
        "fmt"
        "os"
        "time"
    )

2 使用别名

    import (
        std "fmt"
    )


#####命名约定
使用大小写来区分 *常量，变量，类型，接口，结构 或函数*是共有还是私有

例如：
1. 函数名称 首字母小写: private
2. 函数名称 首字母大写: public


[学习资料地址](http://edu.51cto.com/lesson/id-32302.html)




