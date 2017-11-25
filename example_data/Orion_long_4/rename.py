import os

obname="oril04_wa_"
endname=".txt"

files = [f for f in os.listdir('.') if os.path.isfile(f)]
files = [x for x in files if obname in x]

print(len(files))

for i in range(int(len(files)/2)):
	i += 1
	if i<10:
		scan="scan000"+str(i)
		offscan = "offscan000"+str(i)
	else:
		scan="scan00"+str(i)
		offscan = "offscan00" + str(i)

	print('mv ' + obname + scan + endname + ' ' + obname+'scan'+str(i)+endname)
	print('mv ' + obname + offscan + endname + ' ' + obname+'offscan'+str(i)+endname)
	os.system('mv ' + obname + scan + endname + ' ' + obname+'scan'+str(i)+endname)
	os.system('mv ' + obname + offscan + endname + ' ' + obname+'offscan'+str(i)+endname)