'''
Quinn Nguyen
UIN: 524002419
CSCE 315-503
Due: September 10, 2018
quinncsce315.py
'''
from contextlib import closing
from socket import socket, AF_INET, SOCK_DGRAM
from socket import *
import sys
import struct
import time
import datetime
from tkinter import *

NTP_PACKET_FORMAT = "!12I"
NTP_DELTA = 2208988800 # 1970-01-01 00:00:00
NTP_QUERY = b'\x1b' + 47 * b'\0'  

#this function is to calculate the sum of time difference
#excluding 5 (time out servers)
def cal_sum(timeDiff):
	sum = 0;
	for diff in timeDiff:
		if diff == 5:
			continue
		sum = sum + diff
	return sum

#This function is query the server list and calculate the greatest discrepancies
def query_server_list(serverlist):
	timeDiff = []
	numTimeOut = 0
	for server in serverlist:
		#query the current server time
		queryServer = ntp_time(server)
		#if there is a time out, append 5 difference value to the array and skip to next loop
		if(queryServer == 0):
			timeDiff.append(5)
			numTimeOut = numTimeOut + 1
			continue

		readTime = time.ctime(queryServer).replace("  "," ");	#read the current server time
		serverTime = datetime.datetime.strptime(readTime, "%a %b %d %H:%M:%S %Y")	

		#query the current local time
		localTime = datetime.datetime.now()
		
		#calculate the difference between server and local time
		diff = abs(serverTime - localTime)
		timeDiff.append(diff.total_seconds())	#append to the vector

	sumDiff = cal_sum(timeDiff)	# sum of all differences

	serverDict = {}	#create a dictionary to keep track of server and discrepancies
	i = 0	#iteration index for server
	maxDiscrep = abs(timeDiff[i] - (sumDiff - timeDiff[i]) / (len(timeDiff) -1 - numTimeOut))	#to keeep track of current greatest discrepancy
	maxDiscrepServer = 'pool.ntp.org'	#initialize a variable
	for server in serverlist:
		if(timeDiff[i] == 5):	#not include timeout servers
			serverDict[server] = 5
			i = i + 1
			continue

		allOtherDiffAvg = (sumDiff - timeDiff[i]) / (len(timeDiff) -1 - numTimeOut)	#calculate difference average of every other
		serverDict[server] = abs(timeDiff[i] - allOtherDiffAvg)	#calculate discrepancy and store it into dict
		if(serverDict[server] > maxDiscrep):	#keep track of the current greatest discrepancy and its respective server
			maxDiscrep = serverDict[server]		
			maxDiscrepServer = server
		i = i + 1

	#print(serverDict)
	print('Greatest discrepancy =', maxDiscrep)
	print('Greatest discrepancy server =',maxDiscrepServer)
	draw_graph(serverDict)
	return


#called to draw the bar graph
def draw_graph(serverDict):
	root = Tk()
	root.title("Bar Graph")

	c_width = 1000
	c_height = 700
	c = Canvas(root, width=c_width, height=c_height)
	c.pack()

	x0 = 0
	y0 = 0
	for key, value in serverDict.items():
		if(value > 1):
			color = "red"
		else:
			color = "green"

		c.create_rectangle(x0, y0, x0 + (value * 100), y0 + 10,fill =color)
		c.create_text(x0 + (value * 100) + 1, y0, text = key + ' = ' + str(value), anchor = NW)
		y0 = y0 + 25

	root.mainloop()
	return

#Given: to query a server
def ntp_time(host="pool.ntp.org", port=123):
	with closing(socket( AF_INET, SOCK_DGRAM)) as s:
		try:
			s.settimeout(5)	#if no response is received in 5s
			s.sendto(NTP_QUERY, (host, port))
			msg, address = s.recvfrom(1024)
		except timeout:
			#print('time out on server',host)
			return 0
			print('go over return')
	unpacked = struct.unpack(NTP_PACKET_FORMAT,
			msg[0:struct.calcsize(NTP_PACKET_FORMAT)])
	return unpacked[10] + float(unpacked[11]) / 2**32 - NTP_DELTA

if __name__ == "__main__":
	'''
	serverList = ['1.us.pool.ntp.org',
				'0.ubuntu.pool.ntp.org',
				'ntp.ubuntu.com']
	'''
	serverList = ['0.us.pool.ntp.org',
				'1.us.pool.ntp.org',
				'2.us.pool.ntp.org',
				'0.ubuntu.pool.ntp.org',
				'1.ubuntu.pool.ntp.org',
				'2.ubuntu.pool.ntp.org',
				'3.ubuntu.pool.ntp.org',
				'ntp.ubuntu.com',
				'time.apple.com',
				'time.windows.com',
				'time1.google.com',
				'time2.google.com',
				'time3.google.com',
				'time4.google.com',
				'ntp1.tamu.edu',
				'ntp2.tamu.edu',
				'ntp3.tamu.edu',
				'ops1.engr.tamu.edu',
				'ops2.engr.tamu.edu',
				'ops3.engr.tamu.edu',
				'ops4.engr.tamu.edu',
				'filer.cse.tamu.edu',
				'compute.cse.tamu.edu',
				'linux2.cse.tamu.edu',
				'dns1.cse.tamu.edu',
				'dns2.cse.tamu.edu',
				'dhcp1.cse.tamu.edu',
				'dhcp2.cse.tamu.edu']
	query_server_list(serverList)