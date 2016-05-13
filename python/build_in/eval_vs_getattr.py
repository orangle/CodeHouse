#coding:utf-8

class Test(object):

    def test(self, a, b):
        pass

    def docall_eval(self, dmsg):
        docall = "self."+dmsg["func"]+"("
        for k,v in dmsg["para"].items():
            docall =docall + k + "=" + repr(v) + ","
        docall=docall[0:-1]
        docall = docall+")"
        eval(docall)

    def docall_getattr(self, fundict):
        methd = getattr(self, fundict['func'])
        methd(**fundict.get("para", {}))

def test_eval(dmsg):
    t = Test()
    for i in xrange(1000000):
        try:
            t.docall_eval(dmsg)
        except:
            pass

def test_getattr(dmsg):
    t = Test()
    for i in xrange(1000000):
        try:
            t.docall_getattr(dmsg)
        except:
            pass

if __name__ == "__main__":
    dmsg = {"func": "test1", "para": {"a": "xxxxx", "b":"ddddd"}}
    dmsg = {"func": "test", "para": {"a": "xxxxx", "b":"ddddd"}}

    test_eval(dmsg)
    #test_getattr(dmsg)
