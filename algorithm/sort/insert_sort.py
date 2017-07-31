# coding:utf-8

def insert_sort(l):
    N = len(l)
    for i in range(1, N):
        for j in range(i):
            if l[i] < l[j]:
                l[i], l[j] = l[j], l[i]
                print l
        print '\n'
    return l

if __name__ == '__main__':
    l = [10, 2, 11, 4, 3, 6, 9, 2, 7, 61]
    print insert_sort(l)
