#!/usr/bin/env python
# -*- coding: utf-8 -*-
#python2.7x
#split_num_str.py  @2014-07-25
#author: orangleliu
'''
1111|00001-00004,00006-00007,00009#1113|000019#1112|00003,000020
这种字符传的解析
最侯的解析结果是一系列的元组

[('1111','00001'),
('1111','00002'),
('1111','00006'),
('1111','00007'),
('1111','00009'),
('1113','000019'),
('1112','00003'),
('1112','000020')]

分隔符 #代表一个大单元
             |  代表类别和内容
             ,  代表一个连续单元
             -  代表连续数字中间省略
'''

def parse_the_str_num(str_num):
    cate = str_num.strip().split('#')
    parse_res = []
    for ca in cate:
        categ = ca.split('|')[0]
        num_list_str = ca.split("|")[1]
        for i in parse_num_list_str(num_list_str):
            parse_res.append((categ, i))
    return parse_res

#对连续数字解析
def parse_num_list_str(num_str):
    num_groups = num_str.split(",")
    num_list = []
    for group in num_groups:
        start_end = group.split('-')
        if len(start_end)>1:
            #00001-00003 怎么扩充
            #补0
            end = start_end[1]
            start = start_end[0]
            bu = len(end)
            pos = int(end) - int(start)
            for i in range(pos+1):
                num_list.append((bu-len(str(int(start)+i)))*'0'+str(int(start)+i) )
        else:
            num_list.append(group)
    return num_list


test = "1111|00001-00004,00006-00007,00009#1113|000019#1112|00003,000020"
#test
print parse_the_str_num(test)

tes1 = "00001-00002,00006-00007,00009"
#print parse_num_list_str(tes1)



