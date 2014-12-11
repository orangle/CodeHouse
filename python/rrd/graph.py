#-*-coding:utf-8 -*-
#!/usr/bin/python
#author: orangleliu@gmail.com

import rrdtool
import time 
import datetime 

title = "MyPc network trafic flow "+str(datetime.datetime.now().date())

rrdtool.graph("Flow.png", "--start", "-1d", "--vertical-label=Bytes/s", \
        "--x-grid", "MINUTE:12:HOUR:1:HOUR:1:0:%H", \
        "--width", "650", "--height", "230", "--title", title,
        "DEF:inoctets=Flow.rrd:eth0_in:AVERAGE",
        "DEF:outoctets=Flow.rrd:eth0_out:AVERAGE",
        "CDEF:total=inoctets,outoctets,+",
        "LINE1:total#FF8833:Total traffic",
        "AREA:inoctets#00FF00:In traffic",
        "LINE1:outoctets#0000FF:Out traffic",
        "CDEF:inbits=inoctets,8,*",
        "CDEF:outbits=outoctets,8,*",
        "COMMENT:\\r",
        "COMMENT:\\r",
        #"GPRINT:inbits:AVERAGE:Avg In traffic\: %6.21f %Sbps",
        #"COMMENT:  ",
        #"GPRINT:outbits:AVERAGE:Avg Out traffic\: %6.21f %Sbps \\r"i
        )




