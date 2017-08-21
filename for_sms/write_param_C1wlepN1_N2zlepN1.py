#!/usr/bin/env python
import sys, os

mC1 = mN2 = sys.argv[1]
mN1 = sys.argv[2]

print '''######################################################################
## PARAM_CARD AUTOMATICALY GENERATED BY MG5                       ####
######################################################################
###################################
## INFORMATION FOR DSQMIX
###################################
BLOCK DSQMIX # 
      1 1 1.000000e+00 # rrd1x1
      2 2 1.000000e+00 # rrd2x2
      3 3 9.387379e-01 # rrd3x3
      3 6 3.446319e-01 # rrd3x6
      4 4 1.000000e+00 # rrd4x4
      5 5 1.000000e+00 # rrd5x5
      6 3 -3.446319e-01 # rrd6x3
      6 6 9.387379e-01 # rrd6x6
###################################
## INFORMATION FOR FRALPHA
###################################
BLOCK FRALPHA # 
      1 -1.138252e-01 # alp
###################################
## INFORMATION FOR HMIX
###################################
BLOCK HMIX # 
      1 3.576810e+02 # rmuh
      2 9.748624e+00 # tb
      4 1.664391e+05 # ma2
###################################
## INFORMATION FOR MASS
###################################
BLOCK MASS # 
      5 4.889917e+00 # mb
      6 1.750000e+02 # mt
      15 1.777000e+00 # mta
      23 9.118760e+01 # mz
      24 7.982901e+01 # mw
      25 1.108991e+02 # mh01
      35 3.999601e+02 # mh02
      36 3.995839e+02 # ma0
      37 4.078790e+02 # mh
      1000001 5.684411e+03 # set of param :1*msd1, 1*msd2
      1000002 5.611190e+03 # set of param :1*msu1, 1*msu2
      1000005 5.130652e+03 # msd3
      1000006 5.996685e+03 # msu3
      1000011 5.029157e+03 # set of param :1*msl1, 1*msl2
      1000012 5.852583e+03 # set of param :1*msn1, 1*msn2
      1000015 5.344909e+03 # msl3
      1000016 5.847085e+03 # msn3
      1000021 5.077137e+03 # mgo
      1000022 {mN1} # mneu1
      1000023 {mN2} # mneu2
      1000024 {mC1} # mch1
      1000025 -5.637560e+03 # mneu3
      1000035 5.817294e+03 # mneu4
      1000037 5.799393e+03 # mch2
      2000001 5.452285e+03 # set of param :1*msd4, 1*msd5
      2000002 5.492593e+03 # set of param :1*msu4, 1*msu5
      2000005 5.437267e+03 # msd6
      2000006 5.857858e+03 # msu6
      2000011 5.441028e+03 # set of param :1*msl4, 1*msl5
      2000015 5.068678e+03 # msl6
      1 0.000000e+00 # d : 0.0
      2 0.000000e+00 # u : 0.0
      3 0.000000e+00 # s : 0.0
      4 0.000000e+00 # c : 0.0
      11 0.000000e+00 # e- : 0.0
      12 0.000000e+00 # ve : 0.0
      13 0.000000e+00 # mu- : 0.0
      14 0.000000e+00 # vm : 0.0
      16 0.000000e+00 # vt : 0.0
      21 0.000000e+00 # g : 0.0
      22 0.000000e+00 # a : 0.0
      1000014 1.852583e+02 # svm : msn1
      1000013 2.029157e+02 # mul- : msl1
      2000013 1.441028e+02 # mur- : msl4
      1000004 5.611190e+02 # cl : msu1
      2000004 5.492593e+02 # cr : msu4
      1000003 5.684411e+02 # sl : msd1
      2000003 5.452285e+02 # sr : msd4
###################################
## INFORMATION FOR MSD2
###################################
BLOCK MSD2 # 
      1 1 2.736847e+05 # set of param :1*rmd21x1, 1*rmd22x2
      2 2 2.736847e+05 # mg5 will not use this value use instead 1*mdl_rmd21x1
      3 3 2.702620e+05 # rmd23x3
###################################
## INFORMATION FOR MSE2
###################################
BLOCK MSE2 # 
      1 1 1.863063e+04 # set of param :1*rme21x1, 1*rme22x2
      2 2 1.863063e+04 # mg5 will not use this value use instead 1*mdl_rme21x1
      3 3 1.796764e+04 # rme23x3
###################################
## INFORMATION FOR MSL2
###################################
BLOCK MSL2 # 
      1 1 3.815567e+04 # set of param :1*rml21x1, 1*rml22x2
      2 2 3.815567e+04 # mg5 will not use this value use instead 1*mdl_rml21x1
      3 3 3.782868e+04 # rml23x3
###################################
## INFORMATION FOR MSOFT
###################################
BLOCK MSOFT # 
      1 1.013965e+02 # rmx1
      2 1.915042e+02 # rmx2
      3 5.882630e+02 # rmx3
      21 3.233749e+04 # mhd2
      22 -1.288001e+05 # mhu2
###################################
## INFORMATION FOR MSQ2
###################################
BLOCK MSQ2 # 
      1 1 2.998367e+05 # set of param :1*rmq21x1, 1*rmq22x2
      2 2 2.998367e+05 # mg5 will not use this value use instead 1*mdl_rmq21x1
      3 3 2.487654e+05 # rmq23x3
###################################
## INFORMATION FOR MSU2
###################################
BLOCK MSU2 # 
      1 1 2.803821e+05 # set of param :1*rmu21x1, 1*rmu22x2
      2 2 2.803821e+05 # mg5 will not use this value use instead 1*mdl_rmu21x1
      3 3 1.791371e+05 # rmu23x3
###################################
## INFORMATION FOR NMIX
###################################
BLOCK NMIX # 
      1 1 9.863644e-01 # rnn1x1
      1 2 -5.311036e-02 # rnn1x2
      1 3 1.464340e-01 # rnn1x3
      1 4 -5.311861e-02 # rnn1x4
      2 1 9.935054e-02 # rnn2x1
      2 2 9.449493e-01 # rnn2x2
      2 3 -2.698467e-01 # rnn2x3
      2 4 1.561507e-01 # rnn2x4
      3 1 -6.033880e-02 # rnn3x1
      3 2 8.770049e-02 # rnn3x2
      3 3 6.958775e-01 # rnn3x3
      3 4 7.102270e-01 # rnn3x4
      4 1 -1.165071e-01 # rnn4x1
      4 2 3.107390e-01 # rnn4x2
      4 3 6.492260e-01 # rnn4x3
      4 4 -6.843778e-01 # rnn4x4
###################################
## INFORMATION FOR SELMIX
###################################
BLOCK SELMIX # 
      1 1 1.000000e+00 # rrl1x1
      2 2 1.000000e+00 # rrl2x2
      3 3 2.824872e-01 # rrl3x3
      3 6 9.592711e-01 # rrl3x6
      4 4 1.000000e+00 # rrl4x4
      5 5 1.000000e+00 # rrl5x5
      6 3 9.592711e-01 # rrl6x3
      6 6 -2.824872e-01 # rrl6x6
###################################
## INFORMATION FOR SMINPUTS
###################################
BLOCK SMINPUTS # 
      1 1.279340e+02 # aewm1
      3 1.180000e-01 # as
###################################
## INFORMATION FOR SNUMIX
###################################
BLOCK SNUMIX # 
      1 1 1.000000e+00 # rrn1x1
      2 2 1.000000e+00 # rrn2x2
      3 3 1.000000e+00 # rrn3x3
###################################
## INFORMATION FOR TD
###################################
BLOCK TD # 
      3 3 -1.106937e+02 # rtd3x3
###################################
## INFORMATION FOR TE
###################################
BLOCK TE # 
      3 3 -2.540197e+01 # rte3x3
###################################
## INFORMATION FOR TU
###################################
BLOCK TU # 
      3 3 -4.447525e+02 # rtu3x3
###################################
## INFORMATION FOR UMIX
###################################
BLOCK UMIX # 
      1 1 9.168349e-01 # ruu1x1
      1 2 -3.992666e-01 # ruu1x2
      2 1 3.992666e-01 # ruu2x1
      2 2 9.168349e-01 # ruu2x2
###################################
## INFORMATION FOR UPMNS
###################################
BLOCK UPMNS # 
      1 1 1.000000e+00 # rmns1x1
      2 2 1.000000e+00 # rmns2x2
      3 3 1.000000e+00 # rmns3x3
###################################
## INFORMATION FOR USQMIX
###################################
BLOCK USQMIX # 
      1 1 1.000000e+00 # rru1x1
      2 2 1.000000e+00 # rru2x2
      3 3 5.536450e-01 # rru3x3
      3 6 8.327528e-01 # rru3x6
      4 4 1.000000e+00 # rru4x4
      5 5 1.000000e+00 # rru5x5
      6 3 8.327528e-01 # rru6x3
      6 6 -5.536450e-01 # rru6x6
###################################
## INFORMATION FOR VCKM
###################################
BLOCK VCKM # 
      1 1 1.000000e+00 # rckm1x1
      2 2 1.000000e+00 # rckm2x2
      3 3 1.000000e+00 # rckm3x3
###################################
## INFORMATION FOR VMIX
###################################
BLOCK VMIX # 
      1 1 9.725578e-01 # rvv1x1
      1 2 -2.326612e-01 # rvv1x2
      2 1 2.326612e-01 # rvv2x1
      2 2 9.725578e-01 # rvv2x2
###################################
## INFORMATION FOR YD
###################################
BLOCK YD # 
      3 3 1.388402e-01 # ryd3x3
###################################
## INFORMATION FOR YE
###################################
BLOCK YE # 
      3 3 1.008908e-01 # rye3x3
###################################
## INFORMATION FOR YU
###################################
BLOCK YU # 
      3 3 8.928445e-01 # ryu3x3
###################################
## INFORMATION FOR DECAY
###################################
DECAY 6 1.561950e+00 # wt
DECAY 23 2.411433e+00 # wz
DECAY 24 2.002822e+00 # ww
DECAY 25 1.986108e-03 # wh01
DECAY 35 5.748014e-01 # wh02
DECAY 36 6.321785e-01 # wa0
DECAY 37 5.469628e-01 # wh
DECAY 1000001 5.312788e+00 # wsd1
DECAY 1000002 5.477195e+00 # wsu1
DECAY 1000003 5.312788e+00 # wsd2
DECAY 1000004 5.477195e+00 # wsu2
DECAY 1000005 3.736276e+00 # wsd3
DECAY 1000006 2.021596e+00 # wsu3
DECAY 1000011 2.136822e-01 # wsl1
DECAY 1000012 1.498816e-01 # wsn1
DECAY 1000013 2.136822e-01 # wsl2
DECAY 1000014 1.498816e-01 # wsn2
DECAY 1000015 1.483273e-01 # wsl3
DECAY 1000016 1.475190e-01 # wsn3
DECAY 1000021 5.506754e+00 # wgo
DECAY 1000023 2.077700e-02 # wneu2
DECAY 1000024 1.704145e-02 # wch1
DECAY 1000025 -1.915985e+00 # wneu3
DECAY 1000035 2.585851e+00 # wneu4
DECAY 1000037 2.486895e+00 # wch2
DECAY 2000001 2.858123e-01 # wsd4
DECAY 2000002 1.152973e+00 # wsu4
DECAY 2000003 2.858123e-01 # wsd5
DECAY 2000004 1.152973e+00 # wsu5
DECAY 2000005 8.015663e-01 # wsd6
DECAY 2000006 7.373133e+00 # wsu6
DECAY 2000011 2.161216e-01 # wsl4
DECAY 2000013 2.161216e-01 # wsl5
DECAY 2000015 2.699061e-01 # wsl6
DECAY 1 0.000000e+00 # d : 0.0
DECAY 2 0.000000e+00 # u : 0.0
DECAY 3 0.000000e+00 # s : 0.0
DECAY 4 0.000000e+00 # c : 0.0
DECAY 5 0.000000e+00 # b : 0.0
DECAY 11 0.000000e+00 # e- : 0.0
DECAY 12 0.000000e+00 # ve : 0.0
DECAY 13 0.000000e+00 # mu- : 0.0
DECAY 14 0.000000e+00 # vm : 0.0
DECAY 15 0.000000e+00 # ta- : 0.0
DECAY 16 0.000000e+00 # vt : 0.0
DECAY 21 0.000000e+00 # g : 0.0
DECAY 22 0.000000e+00 # a : 0.0
DECAY 1000022 0.000000e+00 # n1 : 0.0
###################################
## INFORMATION FOR QNUMBERS 1000022
###################################
BLOCK QNUMBERS 1000022 #  n1
      1 0 # 3 times electric charge
      2 2 # number of spin states (2s+1)
      3 1 # colour rep (1: singlet, 3: triplet, 8: octet)
      4 0 # particle/antiparticle distinction (0=own anti)
###################################
## INFORMATION FOR QNUMBERS 1000023
###################################
BLOCK QNUMBERS 1000023 #  n2
      1 0 # 3 times electric charge
      2 2 # number of spin states (2s+1)
      3 1 # colour rep (1: singlet, 3: triplet, 8: octet)
      4 0 # particle/antiparticle distinction (0=own anti)
###################################
## INFORMATION FOR QNUMBERS 1000025
###################################
BLOCK QNUMBERS 1000025 #  n3
      1 0 # 3 times electric charge
      2 2 # number of spin states (2s+1)
      3 1 # colour rep (1: singlet, 3: triplet, 8: octet)
      4 0 # particle/antiparticle distinction (0=own anti)
###################################
## INFORMATION FOR QNUMBERS 1000035
###################################
BLOCK QNUMBERS 1000035 #  n4
      1 0 # 3 times electric charge
      2 2 # number of spin states (2s+1)
      3 1 # colour rep (1: singlet, 3: triplet, 8: octet)
      4 0 # particle/antiparticle distinction (0=own anti)
###################################
## INFORMATION FOR QNUMBERS 1000024
###################################
BLOCK QNUMBERS 1000024 #  x1+
      1 3 # 3 times electric charge
      2 2 # number of spin states (2s+1)
      3 1 # colour rep (1: singlet, 3: triplet, 8: octet)
      4 1 # particle/antiparticle distinction (0=own anti)
###################################
## INFORMATION FOR QNUMBERS 1000037
###################################
BLOCK QNUMBERS 1000037 #  x2+
      1 3 # 3 times electric charge
      2 2 # number of spin states (2s+1)
      3 1 # colour rep (1: singlet, 3: triplet, 8: octet)
      4 1 # particle/antiparticle distinction (0=own anti)
###################################
## INFORMATION FOR QNUMBERS 1000021
###################################
BLOCK QNUMBERS 1000021 #  go
      1 0 # 3 times electric charge
      2 2 # number of spin states (2s+1)
      3 8 # colour rep (1: singlet, 3: triplet, 8: octet)
      4 0 # particle/antiparticle distinction (0=own anti)
###################################
## INFORMATION FOR QNUMBERS 35
###################################
BLOCK QNUMBERS 35 #  h2
      1 0 # 3 times electric charge
      2 1 # number of spin states (2s+1)
      3 1 # colour rep (1: singlet, 3: triplet, 8: octet)
      4 0 # particle/antiparticle distinction (0=own anti)
###################################
## INFORMATION FOR QNUMBERS 36
###################################
BLOCK QNUMBERS 36 #  h3
      1 0 # 3 times electric charge
      2 1 # number of spin states (2s+1)
      3 1 # colour rep (1: singlet, 3: triplet, 8: octet)
      4 0 # particle/antiparticle distinction (0=own anti)
###################################
## INFORMATION FOR QNUMBERS 37
###################################
BLOCK QNUMBERS 37 #  h+
      1 3 # 3 times electric charge
      2 1 # number of spin states (2s+1)
      3 1 # colour rep (1: singlet, 3: triplet, 8: octet)
      4 1 # particle/antiparticle distinction (0=own anti)
###################################
## INFORMATION FOR QNUMBERS 1000012
###################################
BLOCK QNUMBERS 1000012 #  sve
      1 0 # 3 times electric charge
      2 1 # number of spin states (2s+1)
      3 1 # colour rep (1: singlet, 3: triplet, 8: octet)
      4 1 # particle/antiparticle distinction (0=own anti)
###################################
## INFORMATION FOR QNUMBERS 1000014
###################################
BLOCK QNUMBERS 1000014 #  svm
      1 0 # 3 times electric charge
      2 1 # number of spin states (2s+1)
      3 1 # colour rep (1: singlet, 3: triplet, 8: octet)
      4 1 # particle/antiparticle distinction (0=own anti)
###################################
## INFORMATION FOR QNUMBERS 1000016
###################################
BLOCK QNUMBERS 1000016 #  svt
      1 0 # 3 times electric charge
      2 1 # number of spin states (2s+1)
      3 1 # colour rep (1: singlet, 3: triplet, 8: octet)
      4 1 # particle/antiparticle distinction (0=own anti)
###################################
## INFORMATION FOR QNUMBERS 1000011
###################################
BLOCK QNUMBERS 1000011 #  el-
      1 -3 # 3 times electric charge
      2 1 # number of spin states (2s+1)
      3 1 # colour rep (1: singlet, 3: triplet, 8: octet)
      4 1 # particle/antiparticle distinction (0=own anti)
###################################
## INFORMATION FOR QNUMBERS 1000013
###################################
BLOCK QNUMBERS 1000013 #  mul-
      1 -3 # 3 times electric charge
      2 1 # number of spin states (2s+1)
      3 1 # colour rep (1: singlet, 3: triplet, 8: octet)
      4 1 # particle/antiparticle distinction (0=own anti)
###################################
## INFORMATION FOR QNUMBERS 1000015
###################################
BLOCK QNUMBERS 1000015 #  ta1-
      1 -3 # 3 times electric charge
      2 1 # number of spin states (2s+1)
      3 1 # colour rep (1: singlet, 3: triplet, 8: octet)
      4 1 # particle/antiparticle distinction (0=own anti)
###################################
## INFORMATION FOR QNUMBERS 2000011
###################################
BLOCK QNUMBERS 2000011 #  er-
      1 -3 # 3 times electric charge
      2 1 # number of spin states (2s+1)
      3 1 # colour rep (1: singlet, 3: triplet, 8: octet)
      4 1 # particle/antiparticle distinction (0=own anti)
###################################
## INFORMATION FOR QNUMBERS 2000013
###################################
BLOCK QNUMBERS 2000013 #  mur-
      1 -3 # 3 times electric charge
      2 1 # number of spin states (2s+1)
      3 1 # colour rep (1: singlet, 3: triplet, 8: octet)
      4 1 # particle/antiparticle distinction (0=own anti)
###################################
## INFORMATION FOR QNUMBERS 2000015
###################################
BLOCK QNUMBERS 2000015 #  ta2-
      1 -3 # 3 times electric charge
      2 1 # number of spin states (2s+1)
      3 1 # colour rep (1: singlet, 3: triplet, 8: octet)
      4 1 # particle/antiparticle distinction (0=own anti)
###################################
## INFORMATION FOR QNUMBERS 1000002
###################################
BLOCK QNUMBERS 1000002 #  ul
      1 2 # 3 times electric charge
      2 1 # number of spin states (2s+1)
      3 3 # colour rep (1: singlet, 3: triplet, 8: octet)
      4 1 # particle/antiparticle distinction (0=own anti)
###################################
## INFORMATION FOR QNUMBERS 1000004
###################################
BLOCK QNUMBERS 1000004 #  cl
      1 2 # 3 times electric charge
      2 1 # number of spin states (2s+1)
      3 3 # colour rep (1: singlet, 3: triplet, 8: octet)
      4 1 # particle/antiparticle distinction (0=own anti)
###################################
## INFORMATION FOR QNUMBERS 1000006
###################################
BLOCK QNUMBERS 1000006 #  t1
      1 2 # 3 times electric charge
      2 1 # number of spin states (2s+1)
      3 3 # colour rep (1: singlet, 3: triplet, 8: octet)
      4 1 # particle/antiparticle distinction (0=own anti)
###################################
## INFORMATION FOR QNUMBERS 2000002
###################################
BLOCK QNUMBERS 2000002 #  ur
      1 2 # 3 times electric charge
      2 1 # number of spin states (2s+1)
      3 3 # colour rep (1: singlet, 3: triplet, 8: octet)
      4 1 # particle/antiparticle distinction (0=own anti)
###################################
## INFORMATION FOR QNUMBERS 2000004
###################################
BLOCK QNUMBERS 2000004 #  cr
      1 2 # 3 times electric charge
      2 1 # number of spin states (2s+1)
      3 3 # colour rep (1: singlet, 3: triplet, 8: octet)
      4 1 # particle/antiparticle distinction (0=own anti)
###################################
## INFORMATION FOR QNUMBERS 2000006
###################################
BLOCK QNUMBERS 2000006 #  t2
      1 2 # 3 times electric charge
      2 1 # number of spin states (2s+1)
      3 3 # colour rep (1: singlet, 3: triplet, 8: octet)
      4 1 # particle/antiparticle distinction (0=own anti)
###################################
## INFORMATION FOR QNUMBERS 1000001
###################################
BLOCK QNUMBERS 1000001 #  dl
      1 -1 # 3 times electric charge
      2 1 # number of spin states (2s+1)
      3 3 # colour rep (1: singlet, 3: triplet, 8: octet)
      4 1 # particle/antiparticle distinction (0=own anti)
###################################
## INFORMATION FOR QNUMBERS 1000003
###################################
BLOCK QNUMBERS 1000003 #  sl
      1 -1 # 3 times electric charge
      2 1 # number of spin states (2s+1)
      3 3 # colour rep (1: singlet, 3: triplet, 8: octet)
      4 1 # particle/antiparticle distinction (0=own anti)
###################################
## INFORMATION FOR QNUMBERS 1000005
###################################
BLOCK QNUMBERS 1000005 #  b1
      1 -1 # 3 times electric charge
      2 1 # number of spin states (2s+1)
      3 3 # colour rep (1: singlet, 3: triplet, 8: octet)
      4 1 # particle/antiparticle distinction (0=own anti)
###################################
## INFORMATION FOR QNUMBERS 2000001
###################################
BLOCK QNUMBERS 2000001 #  dr
      1 -1 # 3 times electric charge
      2 1 # number of spin states (2s+1)
      3 3 # colour rep (1: singlet, 3: triplet, 8: octet)
      4 1 # particle/antiparticle distinction (0=own anti)
###################################
## INFORMATION FOR QNUMBERS 2000003
###################################
BLOCK QNUMBERS 2000003 #  sr
      1 -1 # 3 times electric charge
      2 1 # number of spin states (2s+1)
      3 3 # colour rep (1: singlet, 3: triplet, 8: octet)
      4 1 # particle/antiparticle distinction (0=own anti)
###################################
## INFORMATION FOR QNUMBERS 2000005
###################################
BLOCK QNUMBERS 2000005 #  b2
      1 -1 # 3 times electric charge
      2 1 # number of spin states (2s+1)
      3 3 # colour rep (1: singlet, 3: triplet, 8: octet)
      4 1 # particle/antiparticle distinction (0=own anti)
'''.format(mC1=mC1, mN2=mN2, mN1=mN1)