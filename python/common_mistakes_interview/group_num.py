#-*- coding: utf-8 -*-
#author: zhizhi.liu   @2014-05-21

'''
有一个字典组成的list
[{"C":"1111", "num":"00001" },
{"C":"1111", "num":"00002"},
{"C":"1111", "num":"00003"},
{"C":"1111", "num":"00006"},
{"C":"1111", "num":"00007"},
{"C":"1112", "num":"00003"},
{"C":"1112", "num":"00004"}]

最后要拼接成 "1111|00001-00003, 1111|00006-00007, 1112|00003-00004"
'''

'''
反推：
1->   "1111|00001-00003, 1111|00006-00007, 1112|00003-00004"
2->   {"1111":["00001-00003","00006-00007"], "1112":["00003-00004"]
3->   {"1111":[["00001","00002","00003"],["00006":"00007"]], "1112":[["00003","00004"]] }
4->   {"1111":[[1,2,3],[6,7]], "11112":[[3,4]]}
5->   {"1111":[1,2,3,6,7],"1112":[3,4]}
'''

##原始数据
invoice = [{"C":"1111", "num":"00001" },
{"C":"1111", "num":"00002"},
{"C":"1111", "num":"00006"},
{"C":"1111", "num":"00009"},
{"C":"1111", "num":"00007"},
{"C":"1112", "num":"00003"},
{"C":"1112", "num":"000020"},
{"C":"1113", "num":"000019"}]


##根据k对数据分组
def groupInvoice(invoice_dict):
    res = {}
    for  ice in invoice_dict:
        if ice["C"]  not in  res.keys():
            res[ice["C"]] = []
        res[ice["C"]] = res[ice["C"]] + [ice["num"]]
    return res

##list 数据排序，分组，转化成字符传
def sort_and_format_to_string(v_list):
    kv_dict = {}
    for v in v_list:
        kv_dict[int(v)] = v
    kv_sorted = sorted(list(set(kv_dict)))#默认对字典key排序
    #对list 按数字连续分组
    group_list = group_the_num(kv_sorted)
    res_list = []
    for group in group_list:
        if len(group)==1:
            res_list.append(kv_dict[group[0]])
        elif len(group)>1:
            res_list.append('-'.join((kv_dict[group[0]], kv_dict[group[-1]])))
        else:
            pass
    res_str = ','.join(res_list)
    return res_str

##有序list对连续数字进行分组
def group_the_num(ori_list):
    group_list = []
    pop_list = []

    for n,num in enumerate(ori_list):
        if num in pop_list:
            continue
        temp_list = [num]
        pos = 1
        try:
            while ori_list[n+pos]==num+pos:
                temp_list.append(ori_list[n+pos])
                pop_list.append(ori_list[n+pos])
                pos += 1
        except:
            print u'index out of range'
        group_list.append(temp_list)
    return group_list

##对分组的数据进行排序
def handle_data(invoice):
    res = groupInvoice(invoice)
    #对分组中每个组中的list合并
    for k,v in res.items():
        if len(v)>1:
            new_v = sort_and_format_to_string(v)
            res[k] = new_v  #已经是字符串
        else:
            res[k] = v[0]
    cate_str = [ "%s|%s"%(k,v)  for k,v in res.items()]
    return '#'.join(cate_str)

##test
#group_the_num([1,2,3,6,7,8,10])
print handle_data(invoice)
