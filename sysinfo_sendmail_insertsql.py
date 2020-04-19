#!/usr/bin/env python
#coding=utf-8

#参考：https://blog.csdn.net/wst521/article/details/46831497

import os
import time
import sys
import atexit
import psutil
import re
import MySQLdb

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr

#print "Welcome,current system is",os.name," 3 seconds late start to get data"
time.sleep(1)

line_num = 1

tstamp = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
#function of Get cpu state
def getCPUstate(interval=1):
    return (" CPU:"+str(psutil.cpu_percent(interval))+"%")

def getMemorystate():
    phymem = psutil.virtual_memory()
    line = "Memory: %5s%% %6s/%s"%(
            phymem.percent,
            str(int((phymem.used-phymem.buffers-phymem.cached)/1024/1024))+"M",
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
            return '%.2f%s'%(value,s)
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
    #tstamp = time.asctime()
    #tstamp = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    #print(global(tstamp))
    global tstamp
    #print(tstamp)
    cpuPercent = cpu_state
    memoryPercentUsage = memory_state
    print (tstamp +" | "+cpuPercent+" | "+
            memoryPercentUsage)
    #total
    print(" NetStates:")
    totalBytesSent = bytes2human(tot_after.bytes_sent)
    totalBytesReceived = bytes2human(tot_after.bytes_recv)
    print(" total bytes:  sent: %-10s received: %s"%(\
        totalBytesSent, \
        totalBytesReceived))
    totalPacketsSent = tot_after.packets_sent
    totalPacketsReceived = tot_after.packets_recv
    print( " total packets:  sent: %-10s received: %s"%(\
        totalPacketsSent, \
        totalPacketsReceived))
    # per-network interface details: let's sort network interfaces so    
    # that the ones which generated more traffic are shown first
    print( " ")
	#——————————————————————————————————————————————————————————————————————
    a1= (tstamp +" | "+cpuPercent+" | "+
            memoryPercentUsage)
    #total
    a2=(" NetStates:")
    a3=(" total bytes:  sent: %-10s received: %s"%(\
        totalBytesSent, \
        totalBytesReceived))
    a4=( " total packets:  sent: %-10s received: %s"%(\
        totalPacketsSent, \
        totalPacketsReceived))
    # per-network interface details: let's sort network interfaces so    
    # that the ones which generated more traffic are shown first
    a5=( " ")
	#——————————————————————————————————————————————————————————————————————
    nic_names = pnic_after.keys()
    #nic_names.sort(key=lambda x: sum(pnic_after[x]), reverse=True)
    loeth0TotalBytesSent = []
    loeth0PerSecBytesSent = []
    loeth0TotalBytesRecv = []
    loeth0PerSecBytesRecv = []
    loeth0TotalPktsSent = []
    loeth0PerSecPktsSent = []
    loeth0TotalPktsRecv = []
    loeth0PerSecPktsRecv = []
    for name in nic_names:
        stats_before = pnic_before[name]
        stats_after = pnic_after[name]
        templ = "%-15s %15s %15s"    
        print(templ % (name, "TOTAL", "PER-SEC"))  
        tempTotalBytesSent = bytes2human(stats_after.bytes_sent)
        tempPerSecBytesSent = bytes2human(stats_after.bytes_sent - stats_before.bytes_sent)
        loeth0TotalBytesSent.append(tempTotalBytesSent)
        loeth0PerSecBytesSent.append(tempPerSecBytesSent)
        print(templ % (
            "bytes-sent",    
            tempTotalBytesSent,  
            tempPerSecBytesSent +
            '/s', 
            ))
        tempTotalBytesRecv = bytes2human(stats_after.bytes_recv)
        tempPerSecBytesRecv = bytes2human(stats_after.bytes_recv- stats_before.bytes_recv)
        loeth0TotalBytesRecv.append(tempTotalBytesRecv)
        loeth0PerSecBytesRecv.append(tempPerSecBytesRecv)
        print(templ % (    
            "bytes-recv",    
            tempTotalBytesRecv,    
            tempPerSecBytesRecv
            + '/s',    
            ))
        tempTotalPktsSent = stats_after.packets_sent
        tempPerSecPktsSent = stats_after.packets_sent - stats_before.packets_sent
        loeth0TotalPktsSent.append(tempTotalPktsSent)
        loeth0PerSecPktsSent.append(tempPerSecPktsSent)
        print(templ % ( 
            "pkts-sent",
            tempTotalPktsSent,
            tempPerSecPktsSent,
            ))
        tempTotalPktsRecv = stats_after.packets_recv
        tempPerSecPktsRecv = stats_after.packets_recv - stats_before.packets_recv
        loeth0TotalPktsRecv.append(tempTotalPktsRecv)
        loeth0PerSecPktsRecv.append(tempPerSecPktsRecv)
        print((templ %(
            "pkts-recv", 
            tempTotalPktsRecv,
            tempPerSecPktsRecv,
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
            loeth0TotalBytesSent[0],  
            loeth0PerSecBytesSent[0] +
				'/s', 
				))
			q13=(templ % (    
				"bytes-recv",    
            loeth0TotalBytesRecv[0],    
            loeth0PerSecBytesRecv[0]
				+ '/s',    
				))
			q14=(templ % ( 
				"pkts-sent",
            loeth0TotalPktsSent[0],
            loeth0PerSecPktsSent[0],
				))
			q15=((templ %(
				"pkts-recv", 
            loeth0TotalPktsRecv[0],
            loeth0PerSecPktsRecv[0],
				)))
			q16=( " ")
        if num == 2:
			q21=(templ % (name, "TOTAL", "PER-SEC"))  
			q22=(templ % (
				"bytes-sent",    
            loeth0TotalBytesSent[1],  
            loeth0PerSecBytesSent[1] +
				'/s', 
				))
			q23=(templ % (    
				"bytes-recv",    
            loeth0TotalBytesRecv[1],    
            loeth0PerSecBytesRecv[1]
				+ '/s',    
				))
			q24=(templ % ( 
				"pkts-sent",
            loeth0TotalPktsSent[1],
            loeth0PerSecPktsSent[1],
				))
			q25=((templ %(
				"pkts-recv", 
            loeth0TotalPktsRecv[1],
            loeth0PerSecPktsRecv[1],
				)))
			q26=( " ")
        num+=1
	#——————————————————————————————————————————————————————————————————————
    '''print(loeth0TotalBytesSent)
    print(loeth0PerSecBytesSent)
    print(loeth0TotalBytesRecv)
    print(loeth0PerSecBytesRecv)
    print(loeth0TotalPktsSent)
    print(loeth0PerSecPktsSent)
    print(loeth0TotalPktsRecv)
    print(loeth0PerSecPktsRecv)'''
    
    '''print('tstamp:'+tstamp+'\\->'+tstamp)#数据时间
    print('cpuPercent:'+cpuPercent+'\\->'+re.search(r"(\.\d*|\d*\.\d*)",cpuPercent).group(0))#CPU使用率-(\.\d*|\d*\.\d*)
    print('memoryPercent:'+memoryPercentUsage+'\\->'+re.search(r"(\.\d*|\d*\.\d*)",memoryPercentUsage).group(0))#内存使用率-(\.\d*|\d*\.\d*)
    print('memoryUsage:'+memoryPercentUsage+'\\->'+re.search(r"\d*M/\d*M",memoryPercentUsage).group(0))#内存使用情况-\d*M/\d*M
    print('totalBytesSent:'+totalBytesSent+'\\->'+re.search(r"(\.\d*|\d*\.\d*)(B|K|M|G|T|P|E|Z|Y)",totalBytesSent).group(0))#发送总字节数-(\.\d*|\d*\.\d*)(B|K|M|G|T|P|E|Z|Y)
    print('totalBytesReceived:'+totalBytesReceived+'\\->'+re.search(r"(\.\d*|\d*\.\d*)(B|K|M|G|T|P|E|Z|Y)",totalBytesReceived).group(0))#接收总字节数-(\.\d*|\d*\.\d*)(B|K|M|G|T|P|E|Z|Y)
    print('totalPacketsSent:'+str(totalPacketsSent)+'\\->'+re.search(r"\d*",str(totalPacketsSent)).group(0))#发送总数据包数-\d*
    print('totalPacketsReceived:'+str(totalPacketsReceived)+'\\->'+re.search(r"\d*",str(totalPacketsReceived)).group(0))#接收总数据包数-\d*
    print('loTotalBytesSent:'+loeth0TotalBytesSent[0]+'\\->'+re.search(r"(\.\d*|\d*\.\d*)(B|K|M|G|T|P|E|Z|Y)",loeth0TotalBytesSent[0]).group(0))#lo发送总字节数-(\.\d*|\d*\.\d*)(B|K|M|G|T|P|E|Z|Y)
    print('loPerSecBytesSent:'+loeth0PerSecBytesSent[0]+'/s'+'\\->'+re.search(r"(\.\d*|\d*\.\d*)(B|K|M|G|T|P|E|Z|Y)",loeth0PerSecBytesSent[0]).group(0)+'/s')#lo每秒发送字节数-(\.\d*|\d*\.\d*)(B|K|M|G|T|P|E|Z|Y)
    print('loTotalBytesRecv:'+loeth0TotalBytesRecv[0]+'\\->'+re.search(r"(\.\d*|\d*\.\d*)(B|K|M|G|T|P|E|Z|Y)",loeth0TotalBytesRecv[0]).group(0))#lo接收总字节数-(\.\d*|\d*\.\d*)(B|K|M|G|T|P|E|Z|Y)
    print('loPerSecBytesRecv:'+loeth0PerSecBytesRecv[0]+'/s'+'\\->'+re.search(r"(\.\d*|\d*\.\d*)(B|K|M|G|T|P|E|Z|Y)",loeth0PerSecBytesRecv[0]).group(0)+'/s')#lo每秒接收字节数-(\.\d*|\d*\.\d*)(B|K|M|G|T|P|E|Z|Y)
    print('loTotalPktsSent:'+str(loeth0TotalPktsSent[0])+'\\->'+re.search(r"\d*",str(loeth0TotalPktsSent[0])).group(0))#lo发送总数据包数-\d*
    print('loPerSecPktsSent:'+str(loeth0PerSecPktsSent[0])+'\\->'+re.search(r"\d*",str(loeth0PerSecPktsSent[0])).group(0))#lo每秒发送数据包数-\d*
    print('loTotalPktsRecv:'+str(loeth0TotalPktsRecv[0])+'\\->'+re.search(r"\d*",str(loeth0TotalPktsRecv[0])).group(0))#lo接收总数据包数-\d*
    print('loPerSecPktsRecv:'+str(loeth0PerSecPktsRecv[0])+'\\->'+re.search(r"\d*",str(loeth0PerSecPktsRecv[0])).group(0))#lo每秒接收数据包数-\d*
    print('eth0TotalBytesSent:'+loeth0TotalBytesSent[1]+'\\->'+re.search(r"(\.\d*|\d*\.\d*)(B|K|M|G|T|P|E|Z|Y)",loeth0TotalBytesSent[1]).group(0))#eth0发送总字节数-(\.\d*|\d*\.\d*)(B|K|M|G|T|P|E|Z|Y)
    print('eth0PerSecBytesSent:'+loeth0PerSecBytesSent[1]+'/s'+'\\->'+re.search(r"(\.\d*|\d*\.\d*)(B|K|M|G|T|P|E|Z|Y)",loeth0PerSecBytesSent[1]).group(0)+'/s')#eth0每秒发送字节数-(\.\d*|\d*\.\d*)(B|K|M|G|T|P|E|Z|Y)
    print('eth0TotalBytesRecv:'+loeth0TotalBytesRecv[1]+'\\->'+re.search(r"(\.\d*|\d*\.\d*)(B|K|M|G|T|P|E|Z|Y)",loeth0TotalBytesRecv[1]).group(0))#eth0接收总字节数-(\.\d*|\d*\.\d*)(B|K|M|G|T|P|E|Z|Y)
    print('eth0PerSecBytesRecv:'+loeth0PerSecBytesRecv[1]+'/s'+'\\->'+re.search(r"(\.\d*|\d*\.\d*)(B|K|M|G|T|P|E|Z|Y)",loeth0PerSecBytesRecv[1]).group(0)+'/s')#eth0每秒接收字节数-(\.\d*|\d*\.\d*)(B|K|M|G|T|P|E|Z|Y)
    print('eth0TotalPktsSent:'+str(loeth0TotalPktsSent[1])+'\\->'+re.search(r"\d*",str(loeth0TotalPktsSent[1])).group(0))#eth0发送总数据包数-\d*
    print('eth0PerSecPktsSent:'+str(loeth0PerSecPktsSent[1])+'\\->'+re.search(r"\d*",str(loeth0PerSecPktsSent[1])).group(0))#eth0每秒发送数据包数-\d*
    print('eth0TotalPktsRecv:'+str(loeth0TotalPktsRecv[1])+'\\->'+re.search(r"\d*",str(loeth0TotalPktsRecv[1])).group(0))#eth0接收总数据包数-\d*
    print('eth0PerSecPktsRecv:'+str(loeth0PerSecPktsRecv[1])+'\\->'+re.search(r"\d*",str(loeth0PerSecPktsRecv[1])).group(0))#eth0每秒接收数据包数-\d*'''
    
    tstamp = tstamp
    cpuPercent = re.search(r"(\.\d*|\d*\.\d*)",cpuPercent).group(0)
    memoryPercent = re.search(r"(\.\d*|\d*\.\d*)",memoryPercentUsage).group(0)
    memoryUsage = re.search(r"\d*M/\d*M",memoryPercentUsage).group(0)
    totalBytesSent = re.search(r"(\.\d*|\d*\.\d*)(B|K|M|G|T|P|E|Z|Y)",totalBytesSent).group(0)
    totalBytesReceived = re.search(r"(\.\d*|\d*\.\d*)(B|K|M|G|T|P|E|Z|Y)",totalBytesReceived).group(0)
    totalPacketsSent = re.search(r"\d*",str(totalPacketsSent)).group(0)
    totalPacketsReceived = re.search(r"\d*",str(totalPacketsReceived)).group(0)
    loTotalBytesSent = re.search(r"(\.\d*|\d*\.\d*)(B|K|M|G|T|P|E|Z|Y)",loeth0TotalBytesSent[0]).group(0)
    loPerSecBytesSent = re.search(r"(\.\d*|\d*\.\d*)(B|K|M|G|T|P|E|Z|Y)",loeth0PerSecBytesSent[0]).group(0)+'/s'
    loTotalBytesRecv = re.search(r"(\.\d*|\d*\.\d*)(B|K|M|G|T|P|E|Z|Y)",loeth0TotalBytesRecv[0]).group(0)
    loPerSecBytesRecv = re.search(r"(\.\d*|\d*\.\d*)(B|K|M|G|T|P|E|Z|Y)",loeth0PerSecBytesRecv[0]).group(0)+'/s'
    loTotalPktsSent = re.search(r"\d*",str(loeth0TotalPktsSent[0])).group(0)
    loPerSecPktsSent = re.search(r"\d*",str(loeth0PerSecPktsSent[0])).group(0)
    loTotalPktsRecv = re.search(r"\d*",str(loeth0TotalPktsRecv[0])).group(0)
    loPerSecPktsRecv = re.search(r"\d*",str(loeth0PerSecPktsRecv[0])).group(0)
    eth0TotalBytesSent = re.search(r"(\.\d*|\d*\.\d*)(B|K|M|G|T|P|E|Z|Y)",loeth0TotalBytesSent[1]).group(0)
    eth0PerSecBytesSent = re.search(r"(\.\d*|\d*\.\d*)(B|K|M|G|T|P|E|Z|Y)",loeth0PerSecBytesSent[1]).group(0)+'/s'
    eth0TotalBytesRecv = re.search(r"(\.\d*|\d*\.\d*)(B|K|M|G|T|P|E|Z|Y)",loeth0TotalBytesRecv[1]).group(0)
    eth0PerSecBytesRecv = re.search(r"(\.\d*|\d*\.\d*)(B|K|M|G|T|P|E|Z|Y)",loeth0PerSecBytesRecv[1]).group(0)+'/s'
    eth0TotalPktsSent = re.search(r"\d*",str(loeth0TotalPktsSent[1])).group(0)
    eth0PerSecPktsSent = re.search(r"\d*",str(loeth0PerSecPktsSent[1])).group(0)
    eth0TotalPktsRecv = re.search(r"\d*",str(loeth0TotalPktsRecv[1])).group(0)
    eth0PerSecPktsRecv = re.search(r"\d*",str(loeth0PerSecPktsRecv[1])).group(0)
    print('————————————————————————————————————————————————————————————————')
	#——————————————————————————————————————————————————————————————————————
    # 打开数据库连接
    db = MySQLdb.connect(host="127.0.0.1", user="username", passwd="password", db="dbname", charset='utf8')

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    creator = "system"
    createDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    modifier = "system"
    modifyDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    insertSQL = "INSERT INTO `dbname`.`tablename`\
    (`RowGuid`, `tstamp`, `cpuPercent`, `memoryPercent`, `memoryUsage`,\
     `totalBytesSent`, `totalBytesReceived`, `totalPacketsSent`,\
     `totalPacketsReceived`, `loTotalBytesSent`, `loPerSecBytesSent`,\
     `loTotalBytesRecv`, `loPerSecBytesRecv`, `loTotalPktsSent`,\
     `loPerSecPktsSent`, `loTotalPktsRecv`, `loPerSecPktsRecv`,\
     `eth0TotalBytesSent`, `eth0PerSecBytesSent`, `eth0TotalBytesRecv`,\
     `eth0PerSecBytesRecv`, `eth0TotalPktsSent`, `eth0PerSecPktsSent`,\
     `eth0TotalPktsRecv`, `eth0PerSecPktsRecv`, `isDeleted`, `creator`,\
     `createDate`, `modifier`, `modifyDate`)\
     VALUES (UUID(), '"+tstamp+"', '"+cpuPercent+"', '"+memoryPercent+"', '"+memoryUsage+"',\
     '"+totalBytesSent+"', '"+totalBytesReceived+"', '"+totalPacketsSent+"',\
     '"+totalPacketsReceived+"', '"+loTotalBytesSent+"', '"+loPerSecBytesSent+"',\
     '"+loTotalBytesRecv+"', '"+loPerSecBytesRecv+"', '"+loTotalPktsSent+"',\
     '"+loPerSecPktsSent+"', '"+loTotalPktsRecv+"', '"+loPerSecPktsRecv+"',\
     '"+eth0TotalBytesSent+"', '"+eth0PerSecBytesSent+"', '"+eth0TotalBytesRecv+"',\
     '"+eth0PerSecBytesRecv+"', '"+eth0TotalPktsSent+"', '"+eth0PerSecPktsSent+"',\
     '"+eth0TotalPktsRecv+"', '"+eth0PerSecPktsRecv+"', false, '"+creator+"',\
     '"+createDate+"', '"+modifier+"', '"+modifyDate+"')"

    print(insertSQL)

    try:
       # 执行sql语句
       cursor.execute(insertSQL)
       # 提交到数据库执行
       db.commit()
       print("\ninsert OK")
    except:
       # 发生错误时回滚
       db.rollback()

    # 关闭数据库连接
    db.close()
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
	smtpObj = smtplib.SMTP()								#实例化对象
	smtpObj.connect(mail_host, 587)							#连接SMTP服务器，服务器地址，端口号
	smtpObj.ehlo()											#向Gamil发送SMTP 'ehlo' 命令
	smtpObj.starttls()										#与上一条一起发送了gmail才可以用
	smtpObj.login(mail_user,mail_pass)						#使用用户名密码登录，gmail使用应用专用密码（Google账号->左侧安全性->登录Google中应用专用密码）
	smtpObj.sendmail(sender, receivers, message.as_string())#所需信息填入 发送邮件
	print "邮件发送成功"				#输出成功提示

except smtplib.SMTPException as e:		#抛出异常
	print "Error: 无法发送邮件"			#输出失败提示
	print(e)							#输出异常提示