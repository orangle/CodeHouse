#coding:utf-8

def simple_string_compress(ss):
    if len(ss) == 0 :
        return None

    count = 1
    res = ""
    for i in range(1, len(ss)):
        if ss[i-1] == ss[i]:
            count += 1
        else:
            res += str(count) if count > 1 else ""
            res += ss[i-1]
            count = 1

    res += str(count)
    res += ss[-1]
    return res

print simple_string_compress("aaaaabbbbaacddd")



