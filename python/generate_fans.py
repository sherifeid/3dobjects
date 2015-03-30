__author__ = 'sherif'

"""
Thingiverse fan adapter generator
This script generates different combinations of fan adapter sizes
"""

import os
import sys
import re
import subprocess
from tempfile import mkstemp
from shutil import move
from shutil import copy
from os import remove, close
from multiprocessing.dummy import Pool
from functools import partial
from subprocess import call
import time
import shutil
import multiprocessing


# functions go here
def replacevar(file_path, varname, varval):
    # this replaces a variable in scad file
    # Create temp file
    try:
        scadfile = open(file_path, 'r')
    except:
        print 'ERROR: cannot open scad file to replace variable!'
        sys.exit(0)

    fh, tmp_path = mkstemp()
    tmpfile = open(tmp_path, 'w')

    for line in scadfile:
        _line = line.strip(' ')
        if _line.startswith(varname):
            # if line starts with the required variable name
            _line = _line.replace(' ', '')
            if _line.startswith(varname+'='):
                # make sure that the line is a variable assignment
                tmpfile.write(varname+'='+str(varval)+';'+'\n')
            else:
                # line starts with the variable name but is not a variable assignment
                tmpfile.write(line)
        else:
            # line doesn't start with the variable name
            tmpfile.write(line)

    tmpfile.close()
    close(fh)
    # Remove original file
    remove(file_path)
    # Move new file
    move(tmp_path, file_path)
# end of functions

tstart = time.time()        # start measuring time

# First we define the different fan dimensions
fanlist = []

# every fan has three parameters [a,b,c], assumed a fan with a square frame
# a : fan size
# b : distance between fan screws
# c : diameter of fan screws
# here's a list of the most popular case fan sizes

fanlist.append([25, 20, 2.8])
fanlist.append([30, 24, 3.4])
fanlist.append([40, 32, 4.3])
fanlist.append([50, 40, 4.3])
fanlist.append([60, 50, 4.3])
fanlist.append([70, 61.5, 4.3])
fanlist.append([80, 71.5, 4.5])
fanlist.append([92, 82.5, 4.5])
fanlist.append([120, 105, 4.5])

# global variables
threads = multiprocessing.cpu_count()             # number of threads to run in parallel

print " Detected " + str(threads) + " CPUs, will spawn " + str(threads) + " threads!"

activethreads = 0       # variable used to track threads

cmdarray = []           # initialize command array to run threads
files2clean = []        # initialize a list of files to cleanup after execution

# prep output directory
stloutdir = 'stlout'
if not os.path.exists(stloutdir):
    os.makedirs(stloutdir)
else:
    shutil.rmtree(stloutdir)
    os.makedirs(stloutdir)

# first do the 0 angle adapters
for i in range(0, len(fanlist)):
    for j in range(i+1, len(fanlist)):
        print 'Converting from fan' + str(i) + ' to fan' + str(j)
        # first we create a new file
        oname = 'adapt_'+str(fanlist[i][0])+'mm_to_'+str(fanlist[j][0])+'mm_at_0_deg'
        oscad = stloutdir + '/' + oname + '.scad'
        ostl = stloutdir + '/' + oname + '.stl'
        try:
            copy('variable_fan_adapter.scad', oscad)
        except:
            print 'ERROR: cannot find source scad file!'
            sys.exit(0)
        # load variables into scad file
        replacevar(oscad, 'd_fan1', fanlist[i][0])
        replacevar(oscad, 'ls_fan1', fanlist[i][1])
        replacevar(oscad, 'ds_fan1', fanlist[i][2])
        replacevar(oscad, 'd_fan2', fanlist[j][0])
        replacevar(oscad, 'ls_fan2', fanlist[j][1])
        replacevar(oscad, 'ds_fan2', fanlist[j][2])
        replacevar(oscad, 'a_mani', 0)
        replacevar(oscad, 'l_mani1', 5)
        cmdarray.append('openscad -o ' + ostl + ' ' + oscad)
        files2clean.append(oscad)

pool = Pool(threads)        # concurrent scad threads to run
for i, returncode in enumerate(pool.imap(partial(call, shell=True), cmdarray)):
    if returncode != 0:
       print("%d command failed: %d" % (i, returncode))

# cleanup after program is complete
for i in files2clean:
    remove(i)

tend = time.time()

print "================================================================"
print " Detected " + str(threads) + " CPUs"
print "STL conversion time is: " + str(round(tend-tstart)) + ' seconds'
print "================================================================"