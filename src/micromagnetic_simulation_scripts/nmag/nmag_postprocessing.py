'''
convertNmagProbe.py
Simple script to convert the output from Nmag NmagProbe tool, to the standard
format we have been using for OOMMF - this is intended to improve compatibility
'''

import numpy
import sys


print 'Converting nmagprobe output to standard format'

#Get ahold our system variables
path = sys.argv[1]
nx = 24
ny = 24

#Create an empty array to store the spatially resolved FT in.
spatXMag = numpy.zeros((4000,(nx * ny * 1)))
spatYMag = numpy.zeros((4000,(nx * ny * 1)))
spatZMag = numpy.zeros((4000,(nx * ny * 1)))

#Open up the file, then iterate through it, getting out each line
inputFile = open(path, 'r')
x_inputData = []
y_inputData = []
z_inputData = []
times = []
for line in inputFile.readlines():
    if len(line) > 5:
        splitLine = line.split(']')[0].split('[')[1].split()
        x_inputData.append(splitLine[0])
        y_inputData.append(splitLine[1])
        z_inputData.append(splitLine[2])
        times.append(line.split()[0])

inputFile.close()

x_inputData = numpy.array(x_inputData)
y_inputData = numpy.array(y_inputData)
z_inputData = numpy.array(z_inputData)

#So then we map the output file structure into one that's more useful for us
for t in range(4000):
    spatXMag[t, : nx*ny] = x_inputData[t*nx*ny : (t+1)*nx*ny]
    spatYMag[t, : nx*ny] = y_inputData[t*nx*ny : (t+1)*nx*ny]
    spatZMag[t, : nx*ny] = z_inputData[t*nx*ny : (t+1)*nx*ny]

#Also we need to extract the frequencies
times = numpy.array(times[0::(nx*ny)], dtype = float)

#Save the spatially resolved magnetisation to files
numpy.save('mxs.npy', spatXMag)
numpy.save('mys.npy', spatYMag)
numpy.save('mzs.npy', spatZMag)
