#coding:utf-8

def lengthOfLongestSubstring(s):
    ans, start, end = 0, 0, 0
    res_start = 0

    countDict = {}
    for c in s:
        end += 1
        countDict[c] = countDict.get(c, 0) + 1
        while countDict[c] > 1:
            countDict[s[start]] -= 1
            start += 1

        if end - start > ans:
            ans = end - start
            res_start = start
        print ans, s[start:end]
    return ans, res_start


print lengthOfLongestSubstring('abcdefdae423412')
