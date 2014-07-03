Openstack  学习笔记
===============


####基本概念<br>
__租户(Tenant)__

>租户是资源的集合，不是指一个用户，如果非要和权限对比就是一个group的感觉(最好不要类比)
>资源的集合，资源的容器，资源的拥有者是租户 <br>

*  计算机中的各种资源
*  早期的版本中叫做project
*  Devstack中默认2个租户：admin 和demo
*  配额包括的方面（instance个数， vcpu个数，内存数量，内部ip和公网ip数量）

查看租户的资源：<br>

    openstack@ubuntu:/etc/nova$ sudo nova quota-show
    ERROR (CommandError): You must provide a username or user id via --os-username, --os-user-id, env[OS_USERNAME] or env[OS_USER_ID]


__用户（User）__

>用户是身份标识，用来做认证<br/>
>用户要属于某个租户<br />


__角色（role）__
>权限的集合，将权限分给具体的用户<br/>
>role是可以嵌套的 语法格式为 **rule:[result]**


__服务(service)__
>Openstack 包含的每个模块都是一个服务<br/>
*  对外提供restful API

查看nove的服务：<br>

    openstack@ubuntu:~/devstack$ source openrc admin admin
    openstack@ubuntu:~/devstack$ nova service-list


