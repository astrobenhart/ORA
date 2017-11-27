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
		# type 1 is bad channels, there is 5% chance of getting bad channels, the number of bad channels is normally
		#   distributed with mean 10 and sd 5. The index of the bad channels are found by taking samples from a uniform
		#   distribution from 0.15 * chans to 0.85 * channels. The amplitude of the bad channels is found by sampling
		#   the absoltute value of a normal distribution of mean 100 and sd 35.
		# type 2 is sharp multichannel narrowband RFI .i|i. . Again there is a %5 chance of getting RFI.
		#   The central peak of the RFi is always at 0.6*chans. The distance between the peaks is normally
		#   distributed with mean 10, sd 2. The amplitude of the central peak is normally distributed with
		#   mean 50, sd 5. The amplitude of the middle set of peaks is 0.5 the central and the outside 0.3 of the central.
		# type 3 is broadband noise with a 5% chance of occurring, where the returned data is just an array of 1s.
		if type == 1:
			if np.random.binomial(1,0.01,1) == 1:
				numofbadchans = np.absolute(np.random.normal(10, 5, 1)).astype(int)
				for i in np.unique(np.absolute(np.random.uniform(int(0.15*chans),int(0.85*chans),numofbadchans[0])).astype(int)):
					data[i] = np.absolute(np.random.normal(100, 35, 1))[0]
				print("Type 1 noise injected")
				return data
			else:
				return data
		if type == 2:
			if np.random.binomial(1, 0.01, 1) == 1:
				distbetweenpeaks = np.absolute(np.random.normal(10,2,1))[0]
				data[int(0.6*chans)] = np.absolute(np.random.normal(50,5,1))[0]
				data[(int(0.6*chans) - int(distbetweenpeaks))] = data[int(0.6*chans)] * 0.5
				data[(int(0.6*chans) + int(distbetweenpeaks))] = data[int(0.6*chans)] * 0.5
				data[(int(0.6*chans) - int(2*distbetweenpeaks))] = data[int(0.6*chans)] * 0.3
				data[(int(0.6*chans) + int(2*distbetweenpeaks))] = data[int(0.6*chans)] * 0.3
				print("Type 2 noise injected")
				return data
			else:
				return data
		if type == 3:
			if np.random.binomial(1, 0.01, 1) == 1:
				data = np.ones(chans)
				print("Type 3 noise injected")
				return data
			else:
				return data

	def AllRFI(chans):
		data = RFIsim(1,chans) + RFIsim(2,chans) + RFIsim(3,chans)
		return data

	def simONdata(bands, chans):
		data2 = []
		for i in range(bands):
			channum = np.arange(0,chans,1)
			data = 1.5*gaussianshape(0.35,0.05,channum) + (1/3)*gaussianshape(0.75,0.05,channum) + baseband(chans) + np.random.normal(0,0.01,chans) + AllRFI(chans)
			data2.extend(data)
		return data2

	def simOFFdata(bands, chans):
		data2 = []
		for i in range(bands):
			data = baseband(chans) + np.random.normal(0,0.01,chans) + AllRFI(chans)
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