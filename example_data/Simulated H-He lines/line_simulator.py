import numpy as np
import matplotlib.pyplot as plt

# This py script will generate data in the same format as the autocorrelators output.
# It will generate ON and OFF source data files containing a bandpass and a H and He line plus noise.

numbands = 8
numchans = 1024
numonoffpairs = 30

def gaussianshape(percentagemean, percentagestd, xrange):
	data = 1 / np.sqrt(2 * np.pi * (percentagestd * int(xrange[-1])) ** 2) * np.exp((-(xrange - (percentagemean * int(xrange[-1]))) ** 2) / (2 * (percentagestd * int(xrange[-1])) ** 2))
	return data

def baseband(chans):
	data = []
	for i in range(chans):
		if i <= (0.15*int(chans)):
			data.append(1*np.exp((-(i-int(0.15*chans))**2)/(2*int(0.05*chans)**2)))
		elif i <= (0.85*int(chans)):
			data.append(data[i-1])
		else:
			data.append(1*np.exp((-(i-int(0.85*chans))**2)/(2*int(0.05*chans)**2)))
	data2 = [i * 5 for i in data]
	return data2

def simONdata(bands, chans, onoffpairs):
	data2 = []
	for i in range(bands):
		channum = np.arange(0,chans,1)
		data = 1.5*gaussianshape(0.35,0.05,channum) + (1/3)*gaussianshape(0.75,0.05,channum) + baseband(chans) + np.random.normal(0,2,chans)
		data2.extend(data)
		return data2

def simOFFdata(bands, chans, onoffpairs):
	for i in range(bands):
		channum = np.arange(0,chans,1)
		data = baseband(chans) + np.random.normal(0,2,chans)
		return data

test1 = simONdata(numbands,numchans,1)
#print(test1)

xaxis = np.linspace(0,128,int(len(test1)))
plt.plot(xaxis,test1)