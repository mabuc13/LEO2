# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import numpy.polynomial.polynomial as poly
import argparse


timeData = []
ampData = []


parser = argparse.ArgumentParser()
parser.add_argument('--n', help='the name/path to the file to analyse')
args = parser.parse_args()

f = open (args.n, "r")


for line in f:
    csv = line.split(',')
    time = float(csv[0])
    amp = float(csv[1])
    timeData.append(time)
    ampData.append(amp)

plt.plot(timeData, ampData, label = "Raw amp data versus time", linestyle="-",marker=".")
title = "A snapchat of the raw data from the oscilloscope while switching at 100Hz with no stress"
plt.title(title)
plt.ylabel('Voltage')
plt.xlabel('Seconds')
plt.show()
