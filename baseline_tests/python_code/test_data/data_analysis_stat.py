# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import numpy.polynomial.polynomial as poly
from math import acos, asin, sqrt, sin, cos, pi, atan
import argparse
from scipy.stats import norm

parser = argparse.ArgumentParser()
parser.add_argument('--n', help='the name/path to the file to analyse')
args = parser.parse_args()

f = open (args.n, "r")

#Variables for plotting
showPlot = True

timeData = []
ampData = []


#First read the data, if the data is above 1.65 it's considered logic high and set to 3.3
#If not, its considered logic low and set to 0.03
for line in f:
    csv = line.split(',')
    time = float(csv[0])
    amp = float(csv[1])

    if amp > 1.65:
        amp = 3.3
    else:
        amp = 0.03
    ampData.append(amp)
    timeData.append(time)
oldTime = timeData[0]
oldAmp = ampData[0]
oldPlotAmp = ampData[0]
oldPlotTime = timeData[0]

ampRefined = []
timeRefined = []
count = 0
#Next is cleaning up, so that there's only the first point where the data goes high, and the last point before it switches and vice versa with low.
#We append the first 2 values no matter what
timeRefined.append(timeData[0])
ampRefined.append(ampData[0])

for i in ampData:

    time = timeData[count]
    amp = ampData[count]
    #print "How do we check this?", oldPlotAmp - amp
    if abs(oldPlotAmp - amp) > 3:
        timeRefined.append(oldTime)
        ampRefined.append(oldAmp)
        timeRefined.append(time)
        ampRefined.append(amp)
        oldPlotAmp = amp
        oldPlotTime = time
    oldAmp = amp
    oldTime = time
    count = count +1

count = 0
first = True
lowIntervals = []
highIntervals = []

#plt.plot(timeRefined, ampRefined, label = "Amp after sorting", linestyle="-",marker=".")
#plt.show()

#We always start our data with a high pulse
for i in ampRefined:
    if i > 1.65:    
        if first:    
            startTime = timeRefined[count]
            first = False
        else:
            endTime = timeRefined[count]
            deltaT = abs(endTime - startTime)
            highIntervals.append(deltaT)
            first = True
    else:
        if first:    
            startTime = timeRefined[count]
            first = False
        else:
            endTime = timeRefined[count]
            deltaT = abs(endTime - startTime)
            #print "deltaT: ", deltaT
            lowIntervals.append(deltaT)
            first = True
    count = count +1

#Find the mean of the high and low flanks
timeSumHigh = 0
timeSumLow = 0
for i in highIntervals:
    timeSumHigh = timeSumHigh + i
for i in lowIntervals:
    timeSumLow = timeSumLow + i
#print "TimesumHigh: ", timeSumHigh
highMean = timeSumHigh/(len(highIntervals))
lowMean = timeSumLow/len(lowIntervals)
#Find the standard deviation of the low and high flanks
highDevSum = 0
lowDevSum = 0
for i in highIntervals:
    highDevSum = highDevSum + (i - highMean)**2

for i in lowIntervals:
    lowDevSum = lowDevSum + (i - lowMean)**2
#print "lowDevSum: ", lowDevSum
lowDev = sqrt((1.0*lowDevSum)/(len(lowIntervals)))
print "Low flank deviation", lowDev

highDev = sqrt((1.0*highDevSum)/(len(highIntervals)))
print "High flank standard deviation", highDev
print "Experiment test inteval: ", timeRefined[len(timeRefined)-1]-timeRefined[0]
print "Number of high flanks: " , len(highIntervals)
print "Number of low flanks: " , len(lowIntervals)
print "High flank mean: ", highMean

print "Low flank mean: ", lowMean
freq = 1/(highMean + lowMean )
print "The frequency was calculated to: ", freq
#normal distribution fitting and histogram plotting

#plt.hist(lowIntervals, bins=50, color='g')

#mu, std = norm.fit(lowIntervals)
#print "mu, std", mu, std
#xmin, xmax = plt.xlim()
#x = np.linspace(xmin, xmax, 100)
#p = norm.pdf(x, mu, std)
#plt.plot(x, p, 'k', linewidth=2)

#data = norm.rvs(10.0, 2.5, size=500)

# Fit a normal distribution to the data:
#mu, std = norm.fit(lowIntervals)
#lowIntervals = lowIntervals*1000

my_new_list = []
for i in highIntervals:
    my_new_list.append(i )


# Plot the histogram.
plt.hist(my_new_list, bins=50, alpha=0.6, color='g')

# Plot the PDF.
#xmin, xmax = plt.xlim()
#x = np.linspace(xmin, xmax, 100)
#p = norm.pdf(x, mu, std)
#plt.plot(x, p, 'k', linewidth=2)
#title = "Fit results: mu = %f,  std = %f" % (mu, std)
#plt.title(title)

plt.show()


#plt.show()
#plt.plot(timeRefined, ampRefined, label = "Amp after sorting", linestyle="-",marker=".")
#plt.show()
