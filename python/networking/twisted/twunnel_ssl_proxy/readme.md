一个PC端可以使用的自由网络代理（科学上网)
==================================

> 提示：需求较多，请谨慎， windows也没测试。 需要国外主机一个，Python比较多的依赖环境，了解Python还有对ss代理原理有一定理解。

用到了Twisted 和 twunnel 这两个Python的库。主要是折腾着玩，不过也挺好用。

浏览器通过sockt5连接 本地代理，本地代理通过ssl隧道转发请求到国外代理，然后就能访问 google等网站了。

1. 浏览器安装 SwitchyOmega，并设置本地的socks5代理（端口就是本地代理的端口）
2. 本地和服务器端都要安装 Twisted 和 twunnel，pip 就能安装
3. 使用 ssl_ca_generate.py 生成ca证书，本地生成也行
4. 配置远程代理 启动服务端代理 twunnel_socks5_server_proxy.py
5. 配置本地代理 启动本地代理，注意权限 twunnel_socks5_local_proxy.py

具体的说明在配置中，都是Python程序，直接 python xx.py就可以运行。osx 测试了下，用起来挺好的。 嘿嘿。


