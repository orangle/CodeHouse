# coding:utf-8
# orangleliu  201602
# 翻转list

def reverse(S, start, end):
    if start < end:
        S[start], S[end] = S[end], S[start]
        reverse(S, start+1, end-1)

L = [1,2]
reverse(L, 0, len(L)-1)
print L
