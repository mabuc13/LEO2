# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import numpy.polynomial.polynomial as poly

timeData = []
ampData = []

f = open ('test2.txt', "r")

for line in f:
    csv = line.split(',')
    time = float(csv[0])
    amp = float(csv[1])
    timeData.append(time)
    ampData.append(amp)

plt.plot(timeData, ampData, label = "Raw amp data versus time", linestyle="-",marker=".")
plt.show()
