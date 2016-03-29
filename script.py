#!/usr/bin/python

import sys, os

del sys.argv[0]
list_of_pairs = []

def extract_features ( lp ):
   for i in lp:
      cmd = "./SMILExtract -C openSMILE-2.1.0/config/IS11_speaker_state.conf -I " + i[1] + " -O " + i[0] + "_audiofile.energy.arff"
      status = os.system(cmd)
      print "Status : ", status
   return

for arg in sys.argv:
   l = arg.split(',')
   list_of_pairs.append(l)

extract_features(list_of_pairs)
