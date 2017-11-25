#This is a simple one time use position switching template for observing RRLs
#To be run natively on the 12 or 30 meter field system

# ALWAYS CHECK WITH TIM NATUSCH, STUART WESTON, OR BEN HART BEFORE STARTING EXPERIMENT


import os
import sys
import time

observationname = "XXXXXX" #6 characters max
antenna = "XXXXXX" #Wa = 12M, Ww = 30M
sourcename = "XXXXXX" #6 characters max
RA = "XXXXXX"
DEC = "XXXXXX"
OFFRA = "XXXXXX"
OFFDEC = "XXXXXX"
slewtime = "XXXXX" #time it takes to slew between on and off source position
freq1 = "XXXXXX" #in MHz
freq2 = "XXXXXX" #in MHz
LO = "XXXXXX" #methanol reciever = 5843 MHz
inttime = "XXXXXX" #in seconds
nscans = "XXXXXX"


################## BACKEND SETUP BLOCK ###################
#IF setup
os.system('inject_snap -w ifa = 1,agc,1')
os.system('inject_snap -w ifb = 2,agc,1')
ifa = os.open('inject_snap -w ifa').read()
ifb = os.open('inject_snap -w ifb').read()
ifagain = ifa.split(',')[4]
ifbgain = ifb.split(',')[4]
os.system('inject_snap -w ifa = 1,'+ifagain+',1')
os.system('inject_snap -w ifb = 1,'+ifbgain+',1')
#Mark5B setup
os.system('inject_snap -w mk5b_mode=ext,0xf0f00000,1')
#DBBC setup
os.system('inject_snap -w form=astro')
freq1_LO = int(freq1) - int(LO) - (16/2)
freq2_LO = int(freq2) - int(LO) - (16/2)
os.system('inject_snap -w bbc01='+freq1_LO+',a,16')
os.system('inject_snap -w bbc02='+freq2_LO+',a,16')
os.system('inject_snap -w bbc05='+freq1_LO+',b,16')
os.system('inject_snap -w bbc06='+freq2_LO+',b,16')
#Log setup
os.system('inject_snap log='+observationname)
###########################################################


#slew to on source
os.system('inject_snap -w source=' + sourcename + ',' + RA + ',' + DEC + ',2000.0')
#Max time it would take to slew to on source
if antenna == "Wa":
    firstslewtime = 900
elif antenna == "Ww":
    firstslewtime = 90
else:
    sys.exit("unknown antenna, please only use Ww or Wa")

time.sleep(900)

for i in range(int(nscans)):
    os.system('inject_snap -w mk5=record=on:scan'+i+':'+observationname+':'+antenna)
    time.sleep(int(inttime))
    os.system('inject_snap -w mk5=record=off')

    #slew to off source
	os.system('inject_snap -w source=' + sourcename + ',' + OFFRA + ',' + OFFDEC + ',2000.0')
    time.sleep(slewtime)
    os.system('inject_snap -w mk5=record=on:offscan' + i + ':' + observationname + ':' + antenna)
    time.sleep(int(inttime))
    os.system('inject_snap -w mk5=record=off')

    #slew to on source
    os.system('inject_snap -w source='+sourcename+','+RA+','+DEC+',2000.0')
    time.sleep(slewtime)

os.system('inject_snap -w source=stow')
os.system('inject_snap -w log=station')