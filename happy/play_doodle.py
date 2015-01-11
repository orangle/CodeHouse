# -*- encoding=utf-8 -*-
#author: orangleliu@gmai.com
#date: 2015-01-10
import autopy
import time
import sys

'''
模拟点击键盘  自动弹奏google doodle 曲子

google doodle 演示地址
http://www.iplaysoft.com/google-guitar-doodle.html

google 的地址 可能需要翻墙
http://www.google.com/logos/2011/lespaul.html

别人整理的源码地址
http://pan.baidu.com/s/1kTmSsrP
不过在本地浏览器直接打开没有声音，在网站上没问题

更多的信息 请搜索 google doodle + 关键词
'''

#隐形的翅膀
yinxingdechibang = "358787 6568321 11186532122 358787 6568321 1118653211"

#小星星
xiaoxingxing = "1155665 4433221 5544332 5544332 1155665 4433221"

#沧海一声笑
canghai = "pouyt uytew wewetyuop ppouyty"

#天空之城
tiankong = "6787807 365685 254573 874477 6787807 365685 34878908 876756 1232352 5878007 678789855 43213 376321 2125"

#国歌
guoge = "qr rrrqwer r yrtyi i yyryiytt o i t y iy iytyr y qwrryyiittw t qr ry yi rtiio i yriiiy r q r yriiiy r q r q r q r r"

#月亮之上
yueliang = "3686 3675 53686565326553 3686 89865 36865326656"

def clickbower(mkey):
    time.sleep(0.5)
    autopy.key.tap(mkey)

if __name__ == "__main__":
    #输入曲子名称 默认是天空之城
    try:
        music = sys.argv[1]
        musicq = eval(music)
    except Exception as e:
        musicq = tiankong

    print "now play music ..... %s"%music
    autopy.mouse.click()
    keys = list(musicq)*2
    print keys
    for i in keys:
        clickbower(i)

