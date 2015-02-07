ngrok  本地反向代理
===============

###什么是ngrok
>ngrok is a reverse proxy that creates a secure tunnel from a public endpoint to a locally running web service. ngrok captures and analyzes all traffic over the tunnel for later inspection and replay.
ngrok是一个反向代理，可以从公网建立一个安全隧道到本地的web服务。ngrok 抓取和分析所有的经过数据，用于之后的检查和重放。

更多的介绍可以去github和官网上查找
1 [github](https://github.com/inconshreveable/ngrok)
2 [官网](https://ngrok.com/)
3 [下载安装](https://ngrok.com/download)
4 [使用指南](https://ngrok.com/usage)

这个工具在主流的系统上都可以使用

###使用
下面是使用小记(wind7)

当时下载的时候不是很好下，百度网盘放了一个

下载之后解压，然后执行

    >ngrok.exe 80

然后出现了：

    ngrok                                                           (Ctrl+C to quit)

    Tunnel Status                 online
    Version                       1.7/1.7
    Forwarding                    http://40984492.ngrok.com -> 127.0.0.1:80
    Forwarding                    https://40984492.ngrok.com -> 127.0.0.1:80
    Web Interface                 127.0.0.1:4040
    # Conn                        0
    Avg Conn Time                 0.00ms

接着我们启动一个web服务在80端口，然后访问http://40984492.ngrok.com 这个网址。
浏览器弹出就是我们本地的web应用，有点像花生壳，嘿嘿。

**127.0.0.1:4040这个地址是干嘛的呢？访问下就知道了**

这里就是请求的监控界面，这里可以看到每个请求的具体参数等等，对于调试非常友好。

![ngrok](/images/ngork_detail.png "ngrok界面")


###小结
Ngrok是一个非常有用的工具，对于开发测试很友好，
当然它还有更多的功能，大家根据需要去看用户手册就好了。







