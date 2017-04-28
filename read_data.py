#!/bin/python3

import numpy as np
import matplotlib.pyplot as plt

rdn = []
filename = '../data/input/random.dat'
with open(filename) as infile:
    for lines in infile:
        if lines:
            data = lines.strip('\n')
            cell = data.split(',')
            if len(cell) == 4:
                rdncell = cell[2].split(':')
                rdn.append(float(rdncell[1]))

plt.hist(rdn)
plt.show()
fig = plt.gcf()
