import os
import numpy as np
import csv
import pandas as pd
import matplotlib.pyplot as plt

filename = "orip01_wa_"
end = ".txt"

files = [f for f in os.listdir('.') if os.path.isfile(f)]
files = [x for x in files if filename in x]
print(files)
print(len(files))



for x in range(1,int((len(files)/2)+1)):
	onread = csv.reader(open(filename+"scan"+str(x)+end,"r"))
	offread = csv.reader(open(filename+"offscan"+str(x)+end,"r"))
	onsource = []
	offsource = []

	for row in onread:
		onsource.append(row)
	for row in offread:
		offsource.append(row)
	if x == 1:
		print(len(onsource))
		aver = [0]*len(onsource)
		aver = np.asarray(aver)

	onsource = np.asarray(onsource)
	offsource = np.asarray(offsource)

	print("av:"+str(len(aver)))
	print("on:"+str(len(onsource)))
	print("off:"+str(len(offsource)))


	aver =((x-1)*aver+(onsource-offsource))/x

xaxis = range(len(onsource))*(64/2064)
plt.plot(xaxis, average)

plt.xlabel('MHz')
plt.ylabel('Amplitude')
plt.title(filename)
plt.savefig(filename+".png")
plt.show()