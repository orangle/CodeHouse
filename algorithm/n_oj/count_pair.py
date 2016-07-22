# -*- coding:utf-8 -*-

#url http://www.nowcoder.com/practice/87d5a092a1d647479103e519a6c0a205?rp=2&ru=/activity/oj&qru=/ta/cracking-the-coding-interview/question-ranking
#朴素的方法

class FindPair:
    def countPairs(self, A, n, tsum):
        # write code here
        to = 0
        for i in range(n):
            for j in range(i+1, n):
                if (A[i] + A[j]) == tsum:
                    to += 1
        return to

p = FindPair()
print p.countPairs([1,2,3,4,5],5,6)
