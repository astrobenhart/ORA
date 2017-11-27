import numpy as np
import sys

# This py script will generate data in the same format as the autocorrelators output.
# It takes 3 inputs, the number of bands, the number of channels in each band, and the number of on of pairs generated
# eg for command line; python line_simulator 8 1024 50
# It will generate ON and OFF source data files containing a bandpass and a H and He line plus noise.

if sys.argv[1] == "-h":
	print("This py script will generate data in the same format as the autocorrelators output.")
	print("It will generate ON and OFF source data files containing a bandpass and a H and He line plus noise.")
	print("")
	print("It takes 3 inputs, the number of bands, the number of channels in each band, and the number of on of pairs generated")
	print("eg for command line; python line_simulator 8 1024 50    will generate 50 8 band 1024 channel on off pairs")
	print("")
else:
	numbands = sys.argv[1]
	numchans = sys.argv[2]
	numonoffpairs = sys.argv[3]

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

	def RFIsim(type, chans):
		data=np.zeros(chans)
		# type 1 is bad channels,
		if type == 1:
			if

	def simONdata(bands, chans):
		data2 = []
		for i in range(bands):
			channum = np.arange(0,chans,1)
			data = 1.5*gaussianshape(0.35,0.05,channum) + (1/3)*gaussianshape(0.75,0.05,channum) + baseband(chans) + np.random.normal(0,0.01,chans)
			data2.extend(data)
		return data2

	def simOFFdata(bands, chans):
		data2 = []
		for i in range(bands):
			data = baseband(chans) + np.random.normal(0,0.01,chans)
			data2.extend(data)
			data2.append(" ")
		return data2

	def makearecording(bands, chans, numonoffpairs):
		for i in range(numonoffpairs):
			on = simONdata(bands,chans)
			off = simOFFdata(bands, chans)
			np.savetxt("ONscan"+str(i)+".txt",on,newline="\n",fmt="%s")
			np.savetxt("OFFscan"+str(i)+".txt",off,newline="\n",fmt="%s")

	makearecording(2,128,50)