# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import numpy.polynomial.polynomial as poly
from math import acos, asin, sqrt, sin, cos, pi, atan
import argparse
from scipy.stats import norm
import string


class Analyzer:

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('--n', help='the name/path to the file to analyse')
        self.parser.add_argument('--p', help ='Use --p if you want the histogram of the period instead of the low and high flanks')
        self.parser.add_argument('--s', help ='Use --s if you want the histogram saved instead of shown')
        self.args = self.parser.parse_args()

        self.f = open(self.args.n, "r")

        self.period_his = False
        if self.args.p:
            self.period_his = True

        self.showPlot = True

        if self.args.s:
            self.showPlot = False

        #Variables for plotting

        self.timeData = []
        self.ampData = []

        # self.oldTime = []
        # self.oldAmp = []
        # self.oldPlatAmp = []
        self.ampRefined = []
        self.timeRefined = []

        self.highDev = 0
        self.lowDev = 0

        self.highMean = 0
        self.lowMean = 0

        self.period_intervals = []
        self.period_mean = 0
        self.period_std = 0

        self.timeunit = ""
        self.time_constant = 0
        self.freq = 0

        self.sample_rate = 0.0
    def sort_outliers(self):

    #First read the data, if the data is above 1.65 it's considered logic high and set to 3.3
    #If not, its considered logic low and set to 0.03
        for line in self.f:
            csv = line.split(',')
            time = float(csv[0])
            amp = float(csv[1])

            if amp > 1.65:
                amp = 3.3
            else:
                amp = 0.03
            self.ampData.append(amp)
            self.timeData.append(time)
        self.oldTime = self.timeData[0]
        self.oldAmp = self.ampData[0]


    def remove_middle_points(self):

        oldPlotAmp = self.ampData[0]
        oldPlotTime = self.timeData[0]
        count = 0
        sample_count = 0
        sample_count_list = []
        #Next is cleaning up, so that there's only the first point where the data goes high, and the last point before it switches and vice versa with low.
        #We append the first 2 values no matter what
        self.timeRefined.append(self.timeData[0])
        self.ampRefined.append(self.ampData[0])

        for i in self.ampData:

            time = self.timeData[count]
            amp = self.ampData[count]
            sample_count += 1
            #print "How do we check this?", oldPlotAmp - amp
            if abs(oldPlotAmp - amp) > 3:
                sample_count_list.append(sample_count)
                sample_count = 0
                self.timeRefined.append(oldTime)
                self.ampRefined.append(oldAmp)
                self.timeRefined.append(time)
                self.ampRefined.append(amp)
                oldPlotAmp = amp
                oldPlotTime = time
            oldAmp = amp
            oldTime = time
            count = count +1

        count = 0
        first = True
        self.lowIntervals = []
        self.highIntervals = []

        #plt.plot(timeRefined, ampRefined, label = "Amp after sorting", linestyle="-",marker=".")
        #plt.show()

        #We always start our data with a high pulse
        for i in self.ampRefined:
            if i > 1.65:
                if first:
                    startTime = self.timeRefined[count]
                    period_start = self.timeRefined[count]
                    first = False
                else:
                    endTime = self.timeRefined[count]
                    deltaT = abs(endTime - startTime)
                    self.highIntervals.append(deltaT)
                    first = True
            else:
                if first:
                    startTime = self.timeRefined[count]
                    first = False
                else:
                    endTime = self.timeRefined[count]
                    deltaT = abs(endTime - startTime)
                    #print "deltaT: ", deltaT
                    self.lowIntervals.append(deltaT)
                    period_end = self.timeRefined[count]
                    delta_period = abs(period_end - period_start)
                    self.period_intervals.append(delta_period)
                    first = True
            count = count +1
        #Calculate the sample rate
        self.sample_rate = sample_count_list[0]/self.highIntervals[0]
    #Find the mean of the high and low flanks
    def do_stats(self):
        timeSumHigh = 0
        timeSumLow = 0
        period_sum = 0
        for i in self.highIntervals:
            timeSumHigh = timeSumHigh + i
        for i in self.lowIntervals:
            timeSumLow = timeSumLow + i

        for i in self.period_intervals:
            period_sum += i

        self.period_mean = period_sum/(len(self.period_intervals))
        print "The sample rate of this data: " , self.sample_rate
        print "Which is " , self.period_mean*self.sample_rate, " samples per period"
        #print "TimesumHigh: ", timeSumHigh
        self.highMean = timeSumHigh/(len(self.highIntervals))
        self.lowMean = timeSumLow/len(self.lowIntervals)
        #Find the standard deviation of the low and high flanks
        highDevSum = 0
        lowDevSum = 0
        period_dev_sum = 0

        for i in self.highIntervals:
            highDevSum = highDevSum + (i - self.highMean)**2

        for i in self.lowIntervals:
            lowDevSum = lowDevSum + (i - self.lowMean)**2

        for i in self.period_intervals:
            period_dev_sum += (i-self.period_mean)**2

        #print "lowDevSum: ", lowDevSum
        self.lowDev = sqrt((1.0*lowDevSum)/(len(self.lowIntervals)-1))
        self.period_std = sqrt((1.0*period_dev_sum)/(len(self.period_intervals)-1))
        self.highDev = sqrt((1.0*highDevSum)/(len(self.highIntervals)-1))

        if self.highMean > 0.001:
            self.timeunit = "Milliseconds"
            self.time_constant = 1000
        elif self.highMean > 0.000001:
            self.timeunit = "Microseconds"
            self.time_constant = 1000000
        else:
            self.timeunit = "Seconds"
            self.time_constant = 1

        self.freq = 1/(self.period_mean)
        self.lowDev *= self.time_constant
        self.highDev *= self.time_constant
        self.period_mean *= self.time_constant
        self.period_std *= self.time_constant
        self.lowMean *= self.time_constant
        self.highMean *= self.time_constant
        print "Low flank deviation", self.lowDev
        print "High flank standard deviation", self.highDev
        print "Experiment test inteval: ", self.timeRefined[len(self.timeRefined)-1]-self.timeRefined[0]
        print "Number of high flanks: " , len(self.highIntervals)
        print "Number of low flanks: " , len(self.lowIntervals)
        print "High flank mean: ", self.highMean

        print "Period mu: ", self.period_mean, " Period std: " , self.period_std
        print "Low flank mean: ", self.lowMean


        print "The frequency was calculated to: ", self.freq
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

    def historgram(self):




        my_new_list = []
        my_low_list = []
        for i in self.highIntervals:
            my_new_list.append(i*self.time_constant )
        for i in self.lowIntervals:
            my_low_list.append(i*self.time_constant)

        plt.style.use('seaborn-deep')
        # Plot the histogram.
        plt.hist([my_new_list, my_low_list], bins=75, label =['High flank duration', 'Low flank duration'])
 
        #plt.hist(my_low_list, bins=100, alpha= 0.6, color='r')
        # Plot the PDF.
        #xmin, xmax = plt.xlim()
        #x = np.linspace(xmin, xmax, 100)
        #p = norm.pdf(x, mu, std)
        #plt.plot(x, p, 'k', linewidth=2)
        title = "High flanks: mu = %f  std = %f  low flanks:\n mu = %f  std = %f  [%s]. Frequency: %i [Hz]" % (self.highMean, self.highDev, self.lowMean, self.lowDev, self.timeunit, self.freq)
        plt.title(title)
        plt.legend(loc='upper right')
        plt.ylabel('Number of occurences')
        plt.xlabel(self.timeunit)
        if self.showPlot:
            plt.show()
        else:
            plt.savefig(self.args.s)  # save the figure to file
            plt.close()
    def period_histogram(self):

        period_list = []
        for i in self.period_intervals:
            period_list.append(i * self.time_constant)
        plt.style.use('seaborn-deep')
        # Plot the histogram.
        plt.hist(period_list, bins=75, label=['Period duration'])
        title = "Period histogram with: mu = %f  std = %f [%s] \n The frequency is: %i [Hz]" % (self.period_mean, self.period_std, self.timeunit, self.freq)
        plt.title(title)
        plt.ylabel('Number of occurences')
        plt.xlabel(self.timeunit)
        plt.legend(loc='upper right')
        if self.showPlot:
            plt.show()
        else:
            plt.savefig(self.args.s)  # save the figure to file
            plt.close()
    #plt.show()
    #plt.plot(timeRefined, ampRefined, label = "Amp after sorting", linestyle="-",marker=".")
    #plt.show()

    def main(self):
       # self.f = open(args.n, "r")
        self.sort_outliers()
        self.remove_middle_points()
        self.do_stats()
        if self.period_his:
            self.period_histogram()
        else:
            self.historgram()


if __name__ == '__main__':
    analy = Analyzer()
    analy.main()
