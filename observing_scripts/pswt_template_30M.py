# ALWAYS CHECK WITH TIM NATUSCH, STUART WESTON, OR BEN HART BEFORE STARTING EXPERIMENT

import sys
import os
from astropy import units as u
from astropy.coordinates import SkyCoord

ob_vars = sys.argv

with open(ob_vars[1]) as fd:
  exec(fd.read())

##### VARS ####
#expname
#sourcename
#antenna
#freq1 - freq8
#bandwidth
#lo
#ra
#dec
#offra
#offdec
#offslewtime
#inttime

#### DEFS ####

def print_freq_error(variable, type):
    if type == 0:
        print(repr(eval(variable)), ' is less than ',lo + 10,' MHz, please increase to be within the range ',lo + 10,' to ',lo + 2048,' MHz')
    if type == 1:
        print(variable, ' is less than ',lo + 10,' MHz, please increase to be within the range ',lo + 10,' to ',lo + 2048,' MHz', repr(eval(variable)))

def remove_values_from_list(the_list, val):
        return [value for value in the_list if value != val]

def check_list_empty_val(yourlist,yourlist_str):
    i=0
    for x in yourlist:
        if str(x) == "":
            print("ERROR: variable",yourlist_str[i],"is empty in", ob_vars[0])
            print("please input a suitable value into",yourlist_str[i])
            sys.exit()
        i += 1

def coords_to_fscoords(coord):
    delete_chars = "hdms"
    fs.coord = coord
    for char in delete_chars: coord = coord.replace(char, '')

    #''.join(c for c in coord if c not in 'hdms')

    return coord

def source_visablilty(ra,dec):


#### LISTIFYING VARIBLES ####

critical_vars=[expname, sourcename, antenna, bandwidth, lo, ra, dec, offra, offdec, offslewtime, inttime]
critical_vars_str=["expname", "sourcename", "antenna", "bandwidth", "lo", "ra", "dec", "offra", "offdec", "offslewtime", "inttime"]
freqs = [freq1, freq2, freq3, freq4, freq5, freq6, freq7, freq8]
freqs = list(map(int, freqs))
freqs = remove_values_from_list(freqs,0)


#### TESTING VARS ####

check_list_empty_val(critical_vars, critical_vars_str)

#subtract LO freq from frequencies
print(freqs)
freqs[:] = [int(x) - int(lo) + int(bandwidth)/2 for x in freqs]

lower_bound = int(lo)+10+int(bandwidth)/2
upper_bound = int(lo)+2048-int(bandwidth)/2

for x in freqs:
    if 18 <= x < 2040:
        print("ERROR: One of your frequencies is outside the range "+str(lower_bound)+" - "+str(upper_bound))
        print("Please update your frequencies to suitable values")
        sys.exit()

fsra=coords_to_fscoords(ra)
print(fsra)

print("Yay, we got all the way through to the end")