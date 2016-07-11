#coding:utf-8
'''
url: http://www.nowcoder.com/practice/f094aed769d84cf3b799033c82fc1bf6?rp=1&ru=/activity/oj&qru=/ta/2016test/question-ranking
题目描述 字符串替换

请你实现一个简单的字符串替换函数。原串中需要替换的占位符为"%s",请按照参数列表的顺序一一替换占位符。若参数列表的字符数大于占位符个数。则将剩下的参数字符添加到字符串的结尾。
给定一个字符串A，同时给定它的长度n及参数字符数组arg和它的大小m，请返回替换后的字符串。保证参数个数大于等于占位符个数。保证原串由大小写英文字母组成，同时长度小于等于500。
测试样例：
"A%sC%sE",7,['B','D','F']
返回："ABCDEF"
'''

class StringFormat:
    def formatString(self, A, n, arg, m):
        # write code here
        c = A.count('%s')
        tmp = A%tuple(arg[:c])
        res = tmp + ''.join(arg[c:m])
        return res
