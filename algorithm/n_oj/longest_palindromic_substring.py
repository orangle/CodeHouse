#coding:utf-8
'''
最长回文子串

if the given string is “forgeeksskeegfor”, the output should be “geeksskeeg”
if the given string is “abaaba”, the output should be “abaaba”
if the given string is “abababa”, the output should be “abababa”
if the given string is “abcbabcbabcba”, the output should be “abcbabcba”

使用朴素解法

回文有两种情况
bab
baab

遍历所有元素，假设每个元素都可能是回文的中心，然后计算回文长度
对比找到最长的回文
'''

class Palindrome:
    def getLongestPalindrome(self, A, n):
        # write code here
        length = len(A)
        max_length = 1
        for i in range(length):
            tmplen1 = self.getPalindrome(A, i, i)
            max_length = max(max_length, tmplen1)
            if i < length-1 and A[i] == A[i+1]:
                tmplen2 = self.getPalindrome(A, i, i+1)
                max_length = max(max_length, tmplen2)
        return max_length

    def getPalindrome(self, A, i, j):
        start = i
        end = j
        if i == j:
            tmplen = 1
        else:
            tmplen = 2

        while(start>0 and end<len(A)-1 and A[start-1] == A[end+1]):
            tmplen += 2
            start -= 1
            end += 1

        #print A[i] if i==j else A[i]+A[j] ,':',A[start:start+tmplen], tmplen
        return tmplen


A = 'baabccc'
p = Palindrome()
print p.getLongestPalindrome(A, len(A))

