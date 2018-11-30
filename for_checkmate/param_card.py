#!/usr/bin/env python
import sys

try:
    slha_file = sys.argv[1]
    pythia = sys.argv[2]
    output = sys.argv[3]
    name = sys.argv[4]
    analysis = sys.argv[5]
    xsect = float(sys.argv[6])
    nev = int(sys.argv[7])
except:
    print '[slha] [pythia] [output] [name] [analysis] [xsect] [nev]'
    exit()

print("""
## General Options
[Parameters]
Name: {name}
Analyses: {analysis}
SLHAFile: {slha_file}
QuietMode: True
OutputDirectory: {output}
OutputExists: overwrite
SkipParamCheck: True

## Process Information (Each new process 'X' must start with [X])
[{name}]
Pythia8Card: {pythia}
XSect: {xsect} fb
MaxEvents: {nev}

""").format(slha_file=slha_file, pythia=pythia, output=output, name=name, analysis=analysis, xsect=xsect, nev=nev)

