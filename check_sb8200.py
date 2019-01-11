#!/usr/bin/python

from bs4 import BeautifulSoup
import urllib2

url = 'http://192.168.100.1/cmconnectionstatus.html'
html = urllib2.urlopen(url).read()
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
print status, startProc, startStat,

# Perfdata

print "|",
for i in range(len(downChannel)):
        dChData = downChannel[i].find_all('td')
        dChNum = dChData[0].string
        dChPow = dChData[4].string.split()
        dChSNR = dChData[5].string.split()
        dChCorr = dChData[6].string
        dChUncorr = dChData[7].string
        print "d_" + dChNum + "_pow=" + dChPow[0],
        print "d_" + dChNum + "_snr=" + dChSNR[0],
        print "d_" + dChNum + "_corr=" + dChCorr,
        print "d_" + dChNum + "_uncorr=" + dChUncorr,

for i in range(len(upChannel)):
        uChData = upChannel[i].find_all('td')
        uChNum = uChData[1].string
        uChPow = uChData[6].string.split()
        print "u_" + uChNum + "_pow=" + uChPow[0],

# Exit Statuses

if status == "OK:":
        exit(0)
else:
        exit(2)
