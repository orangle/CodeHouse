#!/usr/bin/python
#coding:utf-8
# author:51reboot.com
import socket,select
import os,sys,copy

HOST = '0.0.0.0'
PORT = 8089
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)     # 释放端口
s.setblocking(0)                                            # 设置为非阻塞
s.bind((HOST,PORT))
s.listen(10)                                                # 等待对列

# listen: accept -> read -> process -> write -> closing
# accpet: read -> process -> wriet -> closing

# 状态机 模板
STATE_M = {
    -1:{                            # sock
        's':'read',              # sock 状态
        'r':{                       # read 的信息
            'have':0,               # 已读的字节数
            'need':10,              # 要读的字节数
        },
        'w':{                       # write 的数据
            'have':0,               # 已经write 的数据
            'need':0,               # 需要write 的数据
        },
        'd':'',         # 用于存放数据
    },
}

STATE= {}

def state_machine(sock):
    if sock == s:
        # 监听socket
        conn,addr = s.accept()
        s.setblocking(0)                    # 设置为非阻塞
        STATE[conn] = copy.deepcopy(STATE_M[-1])             # 给这个连接赋初值
        R_LIST.append(conn)                 # 将sock加入到 需要R_LIST信息的列表
    else:
        # 已经accept的socket
        stat = STATE[sock]['s']             # 保存 sock 的状态信息
        if stat == 'read':
            #如果状态为read,则需要进行读操作
            if STATE[sock]['r']['need'] == 0:
                #  如果 client 发过来的数据全部读取完了
                R_LIST.remove(sock)                                     # 将sock 需要读取的列表中remove
                STATE[sock]['s'] = 'process'                            # 修改sock的状态
                state_machine(sock)                                     # 进行一次回调
            else:
                one_read = sock.recv(STATE[sock]['r']['need'])              # 读取指定字节数
                STATE[sock]['d'] += one_read                                # 更新读取的字节数
                # 需要重新整理已读取的数据与还需要读取的数据
                STATE[sock]['r']['have'] += len(one_read)
                STATE[sock]['r']['need'] -= len(one_read)
                if STATE[sock]['r']['have'] == 10:
                    # 读完头信息开始读取主体内容
                    STATE[sock]['r']['need'] += int(STATE[sock]['d'])       # 修改接下来需要读取的字节数
                    STATE[sock]['d'] = ''                                   # 清空已接收到的数据
        elif stat == 'process':
            # 读完了client发送的数据后，开始给client返回数据
            response = STATE[sock]['d'][::-1]                               # 反转字符
            STATE[sock]['d'] = "%010d%s" % (len(response),response)         # 更新接收到的数据
            STATE[sock]['w']['need'] = len(STATE[sock]['d'])                # 更新需要发出的字节数
            STATE[sock]['s'] = 'write'                                      # 修改sock的状态为写
            W_LIST.append(sock)                                             # 将sock 加入到 W_LIST
        elif stat == 'write':
            print "wirite", STATE
            # 如果状态为 write，同向client发送数据
            last_have_send = STATE[sock]['w']['have']                       # 保存已发送的字节数
            have_send = sock.send(STATE[sock]['d'][last_have_send:])        # 向client发送数据，返回返回了多少个字节
            STATE[sock]['w']['have'] += have_send                           # 修改已发出的字节
            STATE[sock]['w']['need'] -= have_send                           # 修改需要发出的字节
            if STATE[sock]['w']['need'] == 0 and STATE[sock]['w']['have'] != 0:
                # 如果数据已发完，则关闭sock
                STATE[sock]['s'] = 'closing'
        elif stat == 'closing':
            print "closing", STATE

            # 关闭连接
            STATE.pop(sock)                                                 # 将sock从状态里删除
            try:
                W_LIST.remove(sock)                                             # 将sock从w_list里删除
            except ValueError:
                pass
            sock.close()                                                    # 关闭连接

R_LIST = [s]            # 可读的sock列队
W_LIST = []             # 可写的sock队列
non_stop = True
while True:
    try:
        r_socks,w_socks,err_socks = select.select(R_LIST,W_LIST,[])
    except socket.error,e:
        print e
    for sock in r_socks:
        state_machine(sock)
    for sock in w_socks:
        state_machine(sock)
