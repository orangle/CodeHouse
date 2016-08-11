from twisted.internet import reactor, defer

def callback_func_2(result, previous_data):
    # here we pass the result of the deferred down the callback chain
    # (done synchronously)
    print "calling function 1 on result:%s with previous result:%s" % (result, previous_data)
    return result

def callback_func(result):
    #let's do some asynchronous stuff in this callback
    # simple trick here is to return a deferred from a callback
    # instead of the result itself.
    #
    # so we can do asynchronous stuff here,
    # like firing something 1 second later and have
    # another method processing the result
    print "calling function 1 on result:%s" % result
    d = defer.Deferred()
    reactor.callLater(1, d.callback, "second callback") #
    d.addCallback(callback_func_2, result)
    return d

def do():
    d = defer.Deferred()
    reactor.callLater(1, d.callback, "first callback")
    # 这里 first callback 就是回调方法的 参数，1秒之后执行回调，方法是 callback_func,
    # 参数是 first callback
    d.addCallback(callback_func)
    return d

do()
reactor.run()
