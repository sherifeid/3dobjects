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

# first do the 0 angle adapters
for i in range(0, len(fanlist)):
    for j in range(i+1, len(fanlist)):
        print 'Converting from fan' + str(i) + ' to fan' + str(j)
        # first we create a new file
        oname = 'adapt_'+str(fanlist[i][0])+'mm_to_'+str(fanlist[j][0])+'mm_at_0_deg'
        oscad = oname + '.scad'
        ostl = oname + '.stl'
        try:
            copy('variable_fan_adapter.scad', oscad)
        except:
            print 'ERROR: cannot find source scad file!'
            sys.exit(0)
        replacevar(oscad, 'd_fan1', fanlist[i][0])
        replacevar(oscad, 'ls_fan1', fanlist[i][1])
        replacevar(oscad, 'ds_fan1', fanlist[i][2])
        replacevar(oscad, 'd_fan2', fanlist[j][0])
        replacevar(oscad, 'ls_fan2', fanlist[j][1])
        replacevar(oscad, 'ds_fan2', fanlist[j][2])
        replacevar(oscad, 'a_mani', 0)
        # now we run openscad is batch mode
        print 'running openscad...'
        p = subprocess.Popen(['openscad', '-o', ostl, oscad], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        print 'subprocess Output: ' + out
        print 'subprocess Error: ' + err
        remove(oscad)