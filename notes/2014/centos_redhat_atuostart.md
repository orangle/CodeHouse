Centos 中自启动服务
===============

> 基本上使用yum安装的会自动生成那么一个脚本，如果自己源码安装就没有了

Find out the name of service’s script from /etc/init.d/ directory e.g. mysqld or httpd

Add it to chkconfig

    sudo /sbin/chkconfig --add mysqld
Make sure it is in the chkconfig.

    sudo /sbin/chkconfig --list mysqld
Set it to autostart

    sudo /sbin/chkconfig mysqld on
To stop a service from auto starting on boot

    sudo /sbin/chkconfig mysqld off

如果自己不会写这种启动脚本就需要别的方式了。


