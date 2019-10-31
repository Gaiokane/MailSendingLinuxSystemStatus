#!/usr/bin/env python
#coding=utf-8

#参考：https://blog.csdn.net/wst521/article/details/46831497

import os
import time
import sys
import atexit
import psutil

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr

#print "Welcome,current system is",os.name," 3 seconds late start to get data"
time.sleep(1)

line_num = 1

#function of Get cpu state
def getCPUstate(interval=1):
    return (" CPU:"+str(psutil.cpu_percent(interval))+"%")

def getMemorystate():
    phymem = psutil.virtual_memory()
    line = "Memory: %5s%% %6s/%s"%(
            phymem.percent,
            str(int(phymem.used/1024/1024))+"M",
            str(int(phymem.total/1024/1024))+"M"
            )
    return line
def bytes2human(n):
    """
    >>>bytes2human(10000)
    '9.8k'
    >>>bytes2human(100001221)
    '95.4M'
    """
    symbols = ('K','M','G','T','P','E','Z','Y')
    prefix = {}
    for i ,s in enumerate(symbols):
        prefix[s] = 1 << (i+1)*10
    for s in reversed(symbols):
        if n >=prefix[s]:
            value = float(n) / prefix[s]
            return '%.2f %s'%(value,s)
    return '%.2fB'%(n)
def poll(interval):
    """Retrieve raw stats within an interval window."""
    tot_before = psutil.net_io_counters()
    pnic_before = psutil.net_io_counters(pernic=True)
    #sleep some time
    time.sleep(interval)
    tot_after = psutil.net_io_counters()
    pnic_after = psutil.net_io_counters(pernic=True)
    #get cpu stats
    cpu_state = getCPUstate(interval)
    #get memory
    memory_state = getMemorystate()
    return (tot_before,tot_after,pnic_before,pnic_after,cpu_state,memory_state)
def refresh_window(tot_before,tot_after,pnic_before,pnic_after,cpu_state,memory_state):
    """print stats on screen"""
    #print current time,cpu state,memory
    print (time.asctime() +" | "+cpu_state+" | "+
            memory_state)
    #total
    print(" NetStates:")
    print(" total bytes:  sent: %-10s received: %s"%(\
        bytes2human(tot_after.bytes_sent), \
        bytes2human(tot_after.bytes_recv)))
    print( " total packets:  sent: %-10s received: %s"%(\
        tot_after.packets_sent,\
        tot_after.packets_recv))
    # per-network interface details: let's sort network interfaces so    
    # that the ones which generated more traffic are shown first
    print( " ")
	#——————————————————————————————————————————————————————————————————————
    a1= (time.asctime() +" | "+cpu_state+" | "+
            memory_state)
    #total
    a2=(" NetStates:")
    a3=(" total bytes:  sent: %-10s received: %s"%(\
        bytes2human(tot_after.bytes_sent), \
        bytes2human(tot_after.bytes_recv)))
    a4=( " total packets:  sent: %-10s received: %s"%(\
        tot_after.packets_sent,\
        tot_after.packets_recv))
    # per-network interface details: let's sort network interfaces so    
    # that the ones which generated more traffic are shown first
    a5=( " ")
	#——————————————————————————————————————————————————————————————————————
    nic_names = pnic_after.keys()
    #nic_names.sort(key=lambda x: sum(pnic_after[x]), reverse=True)
    for name in nic_names:
        stats_before = pnic_before[name]
        stats_after = pnic_after[name]
        templ = "%-15s %15s %15s"    
        print(templ % (name, "TOTAL", "PER-SEC"))  
        print(templ % (
            "bytes-sent",    
            bytes2human(stats_after.bytes_sent),  
            bytes2human(stats_after.bytes_sent - stats_before.bytes_sent) +
            '/s', 
            ))
        print(templ % (    
            "bytes-recv",    
            bytes2human(stats_after.bytes_recv),    
            bytes2human(stats_after.bytes_recv- stats_before.bytes_recv)
            + '/s',    
            ))
        print(templ % ( 
            "pkts-sent",
            stats_after.packets_sent,
            stats_after.packets_sent - stats_before.packets_sent,
            ))
        print((templ %(
            "pkts-recv", 
            stats_after.packets_recv,
            stats_after.packets_recv - stats_before.packets_recv,
            )))
        print( " ")
	#——————————————————————————————————————————————————————————————————————
    nic_names = pnic_after.keys()
    #nic_names.sort(key=lambda x: sum(pnic_after[x]), reverse=True)
    num = 1
    for name in nic_names:
        stats_before = pnic_before[name]
        stats_after = pnic_after[name]
        templ = "%-15s %15s %15s"
        if num == 1:
			q11=(templ % (name, "TOTAL", "PER-SEC"))  
			q12=(templ % (
				"bytes-sent",    
				bytes2human(stats_after.bytes_sent),  
				bytes2human(stats_after.bytes_sent - stats_before.bytes_sent) +
				'/s', 
				))
			q13=(templ % (    
				"bytes-recv",    
				bytes2human(stats_after.bytes_recv),    
				bytes2human(stats_after.bytes_recv- stats_before.bytes_recv)
				+ '/s',    
				))
			q14=(templ % ( 
				"pkts-sent",
				stats_after.packets_sent,
				stats_after.packets_sent - stats_before.packets_sent,
				))
			q15=((templ %(
				"pkts-recv", 
				stats_after.packets_recv,
				stats_after.packets_recv - stats_before.packets_recv,
				)))
			q16=( " ")
        if num == 2:
			q21=(templ % (name, "TOTAL", "PER-SEC"))  
			q22=(templ % (
				"bytes-sent",    
				bytes2human(stats_after.bytes_sent),  
				bytes2human(stats_after.bytes_sent - stats_before.bytes_sent) +
				'/s', 
				))
			q23=(templ % (    
				"bytes-recv",    
				bytes2human(stats_after.bytes_recv),    
				bytes2human(stats_after.bytes_recv- stats_before.bytes_recv)
				+ '/s',    
				))
			q24=(templ % ( 
				"pkts-sent",
				stats_after.packets_sent,
				stats_after.packets_sent - stats_before.packets_sent,
				))
			q25=((templ %(
				"pkts-recv", 
				stats_after.packets_recv,
				stats_after.packets_recv - stats_before.packets_recv,
				)))
			q26=( " ")
        num+=1
	#——————————————————————————————————————————————————————————————————————
    return a1,a2,a3,a4,a5,q11,q12,q13,q14,q15,q16,q21,q22,q23,q24,q25,q26

try:
    interval = 0
    #while 1:
    args = poll(interval)
    result = ",".join(str(i) for i in refresh_window(*args))
    #refresh_window(*args)
    #interval = 1
    #print result.replace(",", "\n")

except (KeyboardInterrupt,SystemExit):
    pass

def _format_addr(s):					#格式化邮件地址，因为如果包含中文，需要通过Header对象进行编码。
	name, addr = parseaddr(s)
	return formataddr(( \
		Header(name, 'utf-8').encode(), \
		addr.encode('utf-8') if isinstance(addr, unicode) else addr))

# 第三方 SMTP 服务
mail_host = 'smtp.gmail.com'			#设置服务器
mail_user = '*@gmail.com'				#用户名
mail_pass = '*'							#口令

sender = '*@gmail.com'					#发送邮箱
receivers = '*@gmail.com'				#接收邮件

message = MIMEText(result.replace(",", "\n"), 'plain', 'utf-8')					#邮件正文
message['From'] = _format_addr(u'Linux Server <%s>' % sender)					#发件人昵称
message['To'] =  _format_addr(u'QAQ <%s>' % receivers)							#收件人昵称
message['Subject'] = Header(u'服务器 CPU 内存 网络 使用率 ', 'utf-8').encode()	#邮件主题

try:
	smtpObj = smtplib.SMTP()			#实例化对象
	smtpObj.connect(mail_host, 587)		#连接SMTP服务器，服务器地址，端口号
	smtpObj.ehlo()						#向Gamil发送SMTP 'ehlo' 命令
	smtpObj.starttls()					#与上一条一起发送了gmail才可以用
	smtpObj.login(mail_user,mail_pass)	#使用用户名密码登录，gmail使用应用专用密码（Google账号->左侧安全性->登录Google中应用专用密码）
	smtpObj.sendmail(sender, receivers, message.as_string())#所需信息填入 发送邮件
	print "邮件发送成功"				#输出成功提示

except smtplib.SMTPException as e:		#抛出异常
	print "Error: 无法发送邮件"			#输出失败提示
	print(e)							#输出异常提示