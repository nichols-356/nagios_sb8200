#!/usr/bin/python

from bs4 import BeautifulSoup
import urllib2
import sys

influx = 'influx' in sys.argv
#influx = True
url = 'http://192.168.100.1/cmconnectionstatus.html'
try:
        html = urllib2.urlopen(url).read()
except:
        print "WARNING: Unable to read from URL"
        exit(1)
soup = BeautifulSoup(html)
table = soup.find_all('table')

# Define sections

startup = table[0]
downstream = table[1]
upstream = table[2]

# Break it out

startrows = startup.find_all('tr')
startTitle = startrows[0].find('th').string
startHead = startrows[1].find_all('strong')
startDetail = startrows[3:]

downrows = downstream.find_all('tr')
downTitle = downrows[0].find('th').string
downHead = downrows[1].find_all('strong')
downChannel = downrows[2:]

uprows = upstream.find_all('tr')
upTitle = uprows[0].find('th').string
upHead = uprows[1].find_all('strong')
upChannel = uprows[2:]

# Status

for i in range(len(startDetail)):
        startData = startDetail[i].find_all('td')
        startProc = startData[0].string
        startStat = startData[1].string
        #startComm = startData[2]
        if startStat == "OK":
                status = "OK:"
        elif startStat == "Enabled":
                status = "OK:"
        elif startStat == "Allowed":
                status = "OK:"
        else:
                status = "CRITICAL:"
                break
if not influx:
	print status, startProc, startStat,
	print "|",

# Perfdata

for i in range(len(downChannel)):
        dChData = downChannel[i].find_all('td')
        dChNum = dChData[0].string
        dChPow = dChData[4].string.split()
        dChSNR = dChData[5].string.split()
        dChCorr = dChData[6].string
        dChUncorr = dChData[7].string
	if not influx:
        	print "d_" + dChNum + "_pow=" + dChPow[0],
        	print "d_" + dChNum + "_snr=" + dChSNR[0],
        	print "d_" + dChNum + "_corr=" + dChCorr,
        	print "d_" + dChNum + "_uncorr=" + dChUncorr,
	else:
		print "downlink_channel,interface=" + str(i) + " value="+dChNum
		print "downlink_power,interface=" + str(i) + " value="+dChPow[0]
                print "downlink_snr,interface=" + str(i) + " value="+ dChSNR[0]
                print "downlink_corrected,interface=" + str(i) + " value="+ dChCorr
		print "downlink_uncorrected,interface=" + str(i) + " value="+dChUncorr
for i in range(len(upChannel)):
	uChData = upChannel[i].find_all('td')
        uChNum = uChData[1].string
        uChPow = uChData[6].string.split()
        if not influx:
        	print "u_" + uChNum + "_pow=" + uChPow[0],
	else:
		print "uplink_channel,interface="+ str(i) + " value=" + uChNum
                print "uplink_power,interface="+ str(i) + " value=" + uChPow[0]
# Exit Statuses

if status == "OK:":
        exit(0)
else:
        exit(2)
