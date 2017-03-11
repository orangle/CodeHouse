

在shell中调用lua脚本
```
redis-cli --eval incrset.lua links:counter links:urls , http://malcolmgladwellbookgenerator.com/
```
* links:counter links:urls  是 KEYS 的参数列表
* 逗号后面的url，是 ARGV 的参数列表


还有在redis交互界面中的调用
```
EVAL $incrset.lua 2 links:counter links:url http://malcolmgladwellbookgenerator.com/
```
* 2 表示有2个 KEYS 参数
* 剩下的就是 ARGV 参数


脚本中的return是返回给 redis client的东西

### keys 和 argv 有什么区别呢？
keys的作用类似一个参数，值指向redis中对应的value

```
127.0.0.1:6379> SET name:first lzz
OK
127.0.0.1:6379> EVAL 'return ARGV[1].." "..redis.call("get",KEYS[1])' 1 name:first "Hello"
"Hello lzz"
```

### redis内部中可以用lua的哪些api，redis自己又提供了哪些api呢？

The documentation lists the ones that are loaded; base, table, string, math, struct, cjson, cmsgpack, bitop, redis.sha1hex, ref

### 需要每次传脚本吗？
不用，redis对脚本有cache机制


