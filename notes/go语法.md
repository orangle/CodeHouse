Go语法
======

#####Go的基本类型
###### 简单类型
* 布尔型 bool
    * 长度：1个字节
    * 不可以用数字代替 true 或者 false
* 整型 int/uint
    * 根据操作系统的位数来决定
* 8位整形 int8/uint8
    * 1字节
    *取值范围 -128~127/0~255
* 字节型 byte(int8)
* 16位整形 int16/uint16
    *2字节
    *范围 -32768~32767/0~65535
* 32位整形 int32(rune)/uint32
    *4字节
* 64位整形 int64/uint64
    *8字节
* 浮点型 float32/float64
    * 4/8 字节
    * 精确到7/15小数位

######复杂类型
* 复数 complex64/complex128
    * 8/16 字节
* 其他值类型
    * array，struct，string
* 引用类型
    * slice，map，chan
* 接口类型 interface
* 函数类型 func






