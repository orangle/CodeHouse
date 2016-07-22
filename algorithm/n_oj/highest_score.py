#coding:utf-8
'''
题目描述 最高分是多少 (没有AC)

老师想知道从某某同学当中，分数最高的是多少，现在请你编程模拟老师的询问。当然，老师有时候需要更新某位同学的成绩.
输入描述:
输入包括多组测试数据。
每组输入第一行是两个正整数N和M（0 < N <= 30000,0 < M < 5000）,分别代表学生的数目和操作的数目。
学生ID编号从1编到N。
第二行包含N个整数，代表这N个学生的初始成绩，其中第i个数代表ID为i的学生的成绩
接下来又M行，每一行有一个字符C（只取‘Q’或‘U’），和两个正整数A,B,当C为'Q'的时候, 表示这是一条询问操作，他询问ID从A到B（包括A,B）的学生当中，成绩最高的是多少
当C为‘U’的时候，表示这是一条更新操作，要求把ID为A的学生的成绩更改为B。


输出描述:
对于每一次询问操作，在一行里面输出最高成绩.

输入例子:
5 7
1 2 3 4 5
Q 1 5
U 3 6
Q 3 4
Q 4 5
U 4 5
U 2 9
Q 1 5

输出例子:
5
6
5
9
'''

while True:
    try:
        list1=raw_input().split(' ')
        n = int(list1[0])
        m = int(list1[1])
        list2=raw_input().split(' ')
        new_list2=[]
        for i in list2:
            new_list2.append(int(i))
        list2=new_list2
        list3 = []
        for i in range(m):
            list=raw_input().split(' ')
            list[1]=int(list[1])
            list[2]=int(list[2])
            if list[0]=='Q':
                a = list[1]
                b = list[2]
                if a <= b:
                    max_list = list2[(a - 1):b]
                else:
                    max_list = list2[(b - 1):a]
                list3.append(str(max(max_list)))
            if list[0]=='U':
                list2[list[1]-1]=list[2]
        for i in list3:
            print i
    except:
        break





