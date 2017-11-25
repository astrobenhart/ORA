import os
import numpy as np
import csv
import pandas as pd
import matplotlib.pyplot as plt

filename = "oril01_wa_"
end = ".txt"

files = [f for f in os.listdir('.') if os.path.isfile(f)]
files = [x for x in files if filename in x]
# print(files)
print(len(files))



for x in range(1,int((len(files)/2)+1)):
	onsource = np.loadtxt(filename+"scan"+str(x)+end)
	offsource = np.loadtxt(filename+"offscan"+str(x)+end)

	if x == 1:
		aver = onsource - onsource

	# print("aver"+str(len(aver)))
	# print("on:"+str(len(onsource)))
	# print("off:"+str(len(offsource)))

	diff = onsource - offsource
	aver =((x-1)*aver+diff)/x

flagged = 0

# for data in [onsource,offsource,aver]:
# 	for i in range(len(data)):
# 		if data[i] > (np.median(data) + 2*np.std(data)):
# 			data[i] = 0
# 			flagged += 1
# 		if data[i] < (np.median(data) - 2*np.std(data)):
# 			data[i] = 0
# 			flagged += 1

print("Number of data points flagged in plot: "+str(flagged))
print("median: "+str(np.median(aver)))
print("mean: "+str(np.mean(aver)))
print("std: "+str(np.std(aver)))

xaxis = np.linspace(0,128,int(len(onsource)))
#plt.plot(xaxis, offsource)
#plt.plot(xaxis, onsource)
plt.plot(xaxis, aver)
plt.xlabel('MHz')
plt.ylabel('Amplitude')
plt.title(filename)
plt.savefig(filename+".png")
plt.show()
