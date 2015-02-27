# -*- coding: utf-8 -*-
#python2.7x
#ls.py
#orangleliu  2015-02-14
#简单实现ls命令最长用的基本功能，方面windows下操作
#目录和文件添加颜色区别，添加 h说明，重写封装下

import sys, stat, os
import locale
import time

#simple command line processing to get files (if, list)
if len(sys.argv) == 1:
    files=os.listdir(".")
    #ignore files starting with '.' using list comprehension
    files=[filename for filename in files if filename[0] != '.']
else:
    files=sys.argv[1:]

#Do locale sensitive sort of files to list
locale.setlocale(locale.LC_ALL,'')
files.sort(locale.strcoll)

#setup global variables (dictionary)
now = int(time.time())
recent = now - (6*30*24*60*60) #6 months ago

colours={"default":"",
         "blue":   "\x1b[01;34m",
         "cyan":   "\x1b[01;36m",
         "green":  "\x1b[01;32m",
         "red":    "\x1b[01;05;37;41m"}

#判断控制台是否可以打印颜色
def has_colours(stream):
    if not hasattr(stream, "isatty"):
        return False
    if not stream.isatty():
        return False # auto color only on TTYs
    try:
        #windows也可以安装
        import curses
        curses.setupterm()
        return curses.tigetnum("colors") > 2
    except Exception as e :
        # guess false in case of error
        print "some error %s"%str(e)
        return False

has_colours = has_colours(sys.stdout)

#function to get info from mode
def get_mode_info(mode):

    perms="-"
    colour="default"
    link=""

    if stat.S_ISDIR(mode):
        perms="d"
        colour="blue"
    elif stat.S_ISLNK(mode):
        perms="l"
        colour="cyan"
        link = os.readlink(filename)
        if not os.path.exists(filename):
            colour="red"
    elif stat.S_ISREG(mode):
        if mode & (stat.S_IXGRP|stat.S_IXUSR|stat.S_IXOTH): #bitwise operators
            colour="green"
    mode=stat.S_IMODE(mode)
    for who in "USR", "GRP", "OTH":
        for what in "R", "W", "X":
            #lookup attribute at runtime using getattr
            if mode & getattr(stat,"S_I"+what+who):
                perms=perms+what.lower()
            else:
                perms=perms+"-"
    #return multiple bits of info in a tuple
    return (perms, colour, link)

#Now process each file in list using a for loop
for filename in files:
    try: #exceptions
        #Get all the file info
        stat_info=os.lstat(filename)
    except:
        sys.stderr.write("%s: No such file or directory\n" % filename)
        continue

    perms, colour, link = get_mode_info(stat_info.st_mode)

    nlink = "%4d" % stat_info.st_nlink #formatting strings

    size = "%8d" % stat_info.st_size

    #Get time stamp of file
    ts = stat_info.st_mtime
    if (ts < recent) or (ts > now): #boolean operators
        time_fmt = "%Y-%m -%d %H:%M:%S"
    else:
        time_fmt = "%Y-%m-%d %H:%M:%S"
    time_str = time.strftime(time_fmt, time.gmtime(ts))

    def sizeof_fmt(num, suffix='B'):
        for unit in ['','K','M','G','T','P','E','Z']:
            if abs(num) < 1024.0:
                return "%3.1f%s%s" % (num, unit, suffix)
            num /= 1024.0
        return "%.1f%s%s" % (num, 'Y', suffix)

    #Write the result
    sys.stdout.write("%s %s %s %s  " % (perms,nlink, sizeof_fmt(int(size)), time_str))
    if colours[colour] and has_colours:
        #终端显示颜色
        sys.stdout.write(colours[colour] + filename + "\x1b[00m")
    else:
        sys.stdout.write(filename)

    if link:
        sys.stdout.write(" -> ")
    #print will add newline unless there's a trailing ,
    print link
