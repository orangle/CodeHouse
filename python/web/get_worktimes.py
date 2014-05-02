# -*- coding: utf-8 -*-
#get_workingtimes.py   python2.7.x
#orangleliu@gmail.com    2014-05-02
'''
使用不打开浏览器的方式登录考勤系统，并且获取每天上下班时间，然后进行每天上下班时间计算
'''

import urllib
import urllib2
import cookielib
import re
import datetime


hosturl =  'http://att.xx.com/'
goal_url = 'http://att.xx.com/TRecordList.action'

#用户名
username = 'xx.liu'
#密码
password = '1234'
#统计开始日期
start = '2014-04-01'
#统计结束日期
end = '2014-04-30'


def get_worktime_page(hosturl, goal_url, username, password):
    '''
    登录并且获取所需打卡记录的页面
    '''
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
           'Referer' : '******'}
    login_url = 'http://att.chinacache.com/Login.action'

    cj = cookielib.LWPCookieJar()
    cookie_support = urllib2.HTTPCookieProcessor(cj)
    opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)

    #打开登录界面，并登录
    h = urllib2.urlopen(hosturl)
    postData = {
        'username':username,
        'password':password
    }
    postData = urllib.urlencode(postData)

    request = urllib2.Request(login_url, postData)
    response = urllib2.urlopen(request)
    html = response.read()

    request = urllib2.Request(goal_url)
    response = urllib2.urlopen(request)
    text = response.read()
    return text

def parse_html(text):
    '''
    解析html找出所需要的信息
    '''
    regex = "<input type='hidden' name='TRecordValue_[0-9]+?' value=(.+?)>"
    pattern = re.compile(regex)
    time_list = re.findall(pattern, text)
    day_time_list = []
    for i in time_list:
        try:
            temp = i[2:-2]
            elements = temp.split("','")
            work_date = elements[5]
            start_time = elements[6]
            end_time = elements[7]
            
            work_min = 0
            work_hour = 0
            if start_time and end_time:
                start_time_t = datetime.datetime.strptime(start_time, '%H:%M')
                end_time_t = datetime.datetime.strptime(end_time, '%H:%M')
                work_min = (end_time_t - start_time_t).seconds/60
                work_hour = round(work_min/60.0, 2)
                
            if start_time or end_time:
                day_time_list.append((work_date, start_time, end_time, work_min, work_hour))
        except Exception,e:
            print  'some error happened:  '+ str(i)
            continue 
    return day_time_list
        
        
if __name__ == '__main__':
    text = get_worktime_page(hosturl, goal_url, username, password)
    day_time_list = parse_html(text)
    
    start_day = datetime.datetime.strptime(start, "%Y-%m-%d")
    end_day = datetime.datetime.strptime(end, "%Y-%m-%d")
    
    sum_min = 0
    for i in day_time_list:
        curr_day = datetime.datetime.strptime(i[0], "%Y-%m-%d")
        if start_day<=curr_day<=end_day:
            print i[0], i[1], i[2], i[3], i[4]
            sum_min += i[3]
    t_hour = sum_min/60
    t_min = sum_min%60
    print 'From %s to %s'%(start, end)
    print 'You worked %s hours and %s minutes'%(t_hour, t_min)

