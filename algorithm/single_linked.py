#coding: utf-8
#单链表的实现

class Node(object):

    def __init__(self, value, next=None):
        self.data = value
        self.next = next

    def __str__(self):
        return str(self.data)


class SingleLinked(object):

    def __init__(self):
        self.head = None
        self.tail = None

    def add(self, value):
        node = Node(value, None)
        if self.head is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
        self.tail = node

    def show(self):
        if self.head is None:
            print None
        else:
            curnode = self.head
            while curnode is not  None:
                print curnode.data, '->'
                curnode = curnode.next
            print None

    def remove(self, value):
        curnode = self.head
        prenode = None

        while curnode is not None:
            if curnode.data == value:
                if prenode is not  None:
                    prenode.next = curnode.next
                else:
                    self.head = curnode.next

            prenode = curnode
            curnode = curnode.next


if __name__ == "__main__":
    s = SingleLinked()
    s.add(31)
    s.add(3)
    s.show()

    print 'remove'
    s.remove(31)
    s.remove(3)
    s.show()


