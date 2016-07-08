#coding:utf-8
#python2.7.x
import collections

class LRUcache(object):

    def __init__(self):
        self.max = 5
        self.cache = collections.OrderedDict()

    def get(self, key):
        try:
            value = self.cache.pop(key)
            self.cache['key'] = value
        except:
            value = None

        return value

    def set(self, key, value):
        try:
            self.cache.pop(key)
        except Exception as e:
            if len(self.cache) >= self.max:
                self.cache.popitem(last=False)

        self.cache[key] = value
