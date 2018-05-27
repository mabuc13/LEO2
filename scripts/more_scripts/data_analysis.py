# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import numpy.polynomial.polynomial as poly

f = open ('big_snap.txt', "r")

#Variables for plotting
showPlot = True

timeData = []
ampData = []

oldTime = 0
oldAmp = 0
oldPlotAmp = 0
oldPlotTime = 0
#Cleaning up in the data
for line in f:
    csv = line.split(',')
    time = float(csv[0])
    amp = float(csv[1])
    if (amp > 3.2 and amp < 3.4) or (amp < 0.05 and amp > -0.1):
        ampData.append(amp)
        timeData.append(time)

ampRefined = []
timeRefined = []
count = 0

for i in ampData:
#    csv = line.split(',')
    time = timeData[count]
    amp = ampData[count]
    if abs(oldPlotAmp - amp) > 3.2:
        timeRefined.append(oldTime)
        ampRefined.append(oldAmp)
        timeRefined.append(time)
        ampRefined.append(amp)
        oldPlotAmp = amp
        oldPlotTime = time
       # if amp < 0.07:
        #    timeData.append(oldTime)
         #   ampData.append(oldAmp)
          #  timeData.append(time)
           # ampData.append(amp)
    oldAmp = amp
    oldTime = time
    count = count +1



print "Size of amplitude table: ", len(ampData)

plt.plot(timeRefined, ampRefined, label = "Amp after sorting", linestyle="-",marker=".")
plt.show()