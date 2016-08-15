sockts-ssh代理
=============

用ssh命令更简单，这里还是折腾下，远程服务器开启ssh服务，本地能登录ssh就可以了，假如
ip 45.78.37.246, 端口为 2222, 用户名 lzz 密码 123456

1. 运行 generate.py, 得到 KP.pem
2. 配置 twunnel_ssh_local_proxy.py 里面的配置
3. 启动 twunnel_ssh_local_proxy.py 服务
4. 浏览器 socks5 代理设置为 127.0.0.1 1081端口

然后就能自由访问网络了。。 其实有个国外的vps，科学上网有n种方式呀
