#coding:utf-8

lb = [90, 4, 34, 29, 30, 45, 28, 19, 32, 11]

def msort(lb):
    ''' 递归 '''
    print "Splitting ", lb
    if len(lb) > 1:
        mid = len(lb) / 2
        left = lb[:mid]
        right = lb[mid:]

        msort(left)
        msort(right)

        # 两个有序列表归并
        i = 0
        j = 0
        k = 0
        while i < len(left) and  j < len(right):
            if left[i] < right[j]:
                lb[k] = left[i]
                i = i + 1
            else:
                lb[k] = right[j]
                j = j + 1
            k = k + 1

        #处理有序尾部
        while i < len(left):
            lb[k] = left[i]
            i = i + 1
            k = k + 1

        while j < len(right):
            lb[k] = right[j]
            j = j + 1
            k = k + 1

        print "Merging ", left, right

    print "Merged ", lb

if __name__ == "__main__":
    msort(lb)
    print lb
