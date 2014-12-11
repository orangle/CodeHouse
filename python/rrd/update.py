#-*- coding=utf-8 -*-
#!/usr/bin/python
#author: orangleliu@gmail.com
import rrdtool
import time, psutil,os

rrd_path = os.path.join(os.getcwd(), "Flow.rrd")
total_input_trafic = 103334355 #psutil.net_io_counters()[1]
total_ouput_trafic = 111111    #psutil.net_io_counters()[0]
start_time = int(time.time())

update = rrdtool.updatev(rrd_path, "%s:%s:%s"%(str(start_time), 
    str(total_input_trafic), str(total_ouput_trafic)))

print update
