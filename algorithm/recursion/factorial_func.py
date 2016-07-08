#coding:utf-8
#orangleliu  201502
#阶乘 递归

def factorial(n):
    if n == 0:
        return 1
    else:
        return n*factorial(n-1)

if __name__ == "__main__":
    print factorial(1)
    print factorial(5)
    print factorial(20)
