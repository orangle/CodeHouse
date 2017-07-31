# coding:utf-8

def select_sort(l):
    n = len(l)
    for i in range(n):
        mini = i
        for j in range(i+1, n):
            if l[j] < l[mini]:
                mini = j
        l[i], l[mini] = l[mini], l[i]
        print l
    return l


if __name__ == '__main__':
    l = [10, 2, 11, 4, 3, 6, 9, 2, 7, 61]
    print select_sort(l)
