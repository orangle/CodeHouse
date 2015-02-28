# -*- coding: utf-8 -*-
#python2.7.x
#author: orangleliu

"""
利用QQIP纯真库获取IP对应的地理位置信息
IPLocator: locate IP in the qqwry.dat
    Usage:
        python ip_location.py <ip>

DONE:
#增加命令行参数
#封装接口，提供json格式的返回值

BUG fix：
#linux下正常显示，windows下显示有问题

TODO：
#指定数据库文件的位置
#增加自动升级功能
#某些情况下常驻内存，不用每次打开
"""

import sys 
import socket
import string
import struct
try: 
    import simplejson as json 
except:
    import json

def _p(words):
    return words.decode("utf-8")

class IPLocator(object):
    def __init__(self, ipdbFile="qqwry.dat"):
        self.ipdb = open(ipdbFile, "rb")
        str = self.ipdb.read(8)
        # 纯真数据库全部采用了little-endian字节序
        (self.firstIndex,self.lastIndex) = struct.unpack('II',str)
        # 每条索引长7字节，这里得到索引总个数
        self.indexCount = (self.lastIndex - self.firstIndex)/7+1
        print _p("%s 记录总数: %d 条 "%(self.getVersion(), self.indexCount))

    def getVersion(self):
        s = self.getIpAddr(0xffffff00L)
        return s

    def getAreaAddr(self,offset=0):
        if offset :
            self.ipdb.seek( offset )
        str = self.ipdb.read( 1 )
        (byte,) = struct.unpack('B',str)
        if byte == 0x01 or byte == 0x02:
            p = self.getLong3()
            if p:
                return self.getString( p )
            else:
                return ""
        else:
            self.ipdb.seek(-1,1)
            return self.getString(offset)

    def getAddr(self,offset,ip=0):
        self.ipdb.seek(offset + 4)
        countryAddr = ""
        areaAddr = ""
        str = self.ipdb.read(1)
        (byte,) = struct.unpack('B',str)
        if byte == 0x01:
            countryOffset = self.getLong3()
            self.ipdb.seek(countryOffset)
            str = self.ipdb.read(1)
            (b,) = struct.unpack('B',str)
            if b == 0x02:
                countryAddr = self.getString(self.getLong3())
                self.ipdb.seek(countryOffset + 4)
            else:
                countryAddr = self.getString(countryOffset)
            areaAddr = self.getAreaAddr()
        elif byte == 0x02:
            countryAddr = self.getString(self.getLong3())
            areaAddr = self.getAreaAddr( offset + 8 )
        else:
            countryAddr = self.getString(offset + 4)
            areaAddr = self.getAreaAddr()
        return countryAddr + " " + areaAddr

    def dump(self, first ,last):
        if last > self.indexCount :
            last = self.indexCount
        for index in range(first,last):
            offset = self.firstIndex + index * 7
            self.ipdb.seek(offset)
            buf = self.ipdb.read(7)
            (ip,of1,of2) = struct.unpack("IHB",buf)
            address = self.getAddr(of1 + (of2 << 16))
            #把GBK转为utf-8
            address = unicode(address,'gbk').encode("utf-8")
            print "%d\t%s\t%s" %(index, self.ip2str(ip), \
                address )

    def setIpRange(self,index):
        offset = self.firstIndex + index * 7
        self.ipdb.seek(offset)
        buf = self.ipdb.read(7)
        (self.curStartIp,of1,of2) = struct.unpack("IHB",buf)
        self.curEndIpOffset = of1 + (of2 << 16)
        self.ipdb.seek(self.curEndIpOffset)
        buf = self.ipdb.read(4)
        (self.curEndIp,) = struct.unpack("I",buf)

    def getIpAddr(self,ip):
        L = 0
        R = self.indexCount - 1
        while L < R-1:
            M = (L + R) / 2
            self.setIpRange(M)
            if ip == self.curStartIp:
                L = M
                break
            if ip > self.curStartIp:
                L = M
            else:
                R = M
        self.setIpRange(L)
        #version information,255.255.255.X,urgy but useful
        if ip&0xffffff00L == 0xffffff00L:
            self.setIpRange(R)
        if self.curStartIp <= ip <= self.curEndIp:
            address = self.getAddr(self.curEndIpOffset)
            #把GBK转为utf-8
            address = unicode(address,'gbk').encode("utf-8")
        else:
            address = _p("未找到该IP的地址")
        return address

    def getIpRange(self,ip):
        self.getIpAddr(ip)
        range = self.ip2str(self.curStartIp) + ' - ' \
            + self.ip2str(self.curEndIp)
        return range

    def getString(self,offset = 0):
        if offset :
            self.ipdb.seek(offset)
        str = ""
        ch = self.ipdb.read(1)
        (byte,) = struct.unpack('B',ch)
        while byte != 0:
            str = str + ch
            ch = self.ipdb.read(1)
            (byte,) = struct.unpack('B',ch)
        return str

    def ip2str(self,ip):
        return str(ip>>24)+'.'+str((ip>>16)&0xffL)+'.' \
            +str((ip>>8)&0xffL)+'.'+str(ip&0xffL)

    def str2ip(self,s):
        (ip,) = struct.unpack('I',socket.inet_aton(s))
        return ((ip>>24)&0xffL)|((ip&0xffL)<<24) \
            |((ip>>8)&0xff00L)|((ip&0xff00L)<<8)

    def getLong3(self,offset = 0):
        if offset :
            self.ipdb.seek(offset)
        str = self.ipdb.read(3)
        (a,b) = struct.unpack('HB',str)
        return (b << 16) + a
    
    def getJsonAddr(self, ip_str):
        addr = _p(self.getIpAddr(self.str2ip(ip_str)))
        data = {"ip": ip_str, "address":addr}
        return json.dumps(data)
    
    
#直接返回地址
ipl = IPLocator("qqwry.dat")
def getAddress(ip_str):
    return _p(ipl.getIpAddr(ipl.str2ip(ip_str)))

    
def main():
    #默认路径跟脚本一个文件夹
    import argparse
    parser = argparse.ArgumentParser(description=u"纯真IP数据库查询")
    parser.add_argument("ip",nargs="+", help=u"要查询的IP")
    parser.add_argument("-d", '--detail', action="store_true",default=False,
                        help=u"详细输出结果")
    args = parser.parse_args()
    if not (args.ip):
        parser.print_help
        sys.exit(0)

    IPL = IPLocator("qqwry.dat")
    is_detail = args.detail 
    
    print ""
    for ip in args.ip:
        address = IPL.getIpAddr(IPL.str2ip(ip))
        print _p("%s %s"%(ip,address))
        if is_detail:
            range = IPL.getIpRange(IPL.str2ip(ip))
            print _p("所在网段: %s" %(range,))
    
if __name__ == "__main__":
    main()
