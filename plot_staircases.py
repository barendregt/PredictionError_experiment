from __future__ import division

from matplotlib import pyplot as pl 
import numpy as np 
import cPickle as pickle
import glob
import seaborn as sn
import pandas as pd
import sys,os
sys.path.append( 'exp_tools' )

from Staircase import ThreeUpOneDownStaircase
from IPython import embed as shell


def plot_staircases(initials,run_nr):

 	stairs = ['red','green','45', '135']

 	# Load staircase data
 	staircases = pickle.load(open('data/' + initials + '_staircase.pickle','rb'))

 	# Compute average performance over time
 	percent_correct = list()
	stair_values = list()
	responses = list()
	#n_responses =list()
	
 	for ii in range(len(staircases)):

 		responses = staircases[ii].past_answers
		#n_responses.append()
		
		#stair_values.append(staircases[ii].test_values)
		
 		percent_correct.append(np.cumsum(np.array(responses)) / np.arange(1,len(responses)+1))
	
		
 	# Plot average resp correct over time

# 	f = pl.figure()
# 	for s in range(len(stairs)):
# 		pl.plot(percent_correct[s],'-')
# 	pl.legend(stairs)
 
	f = pl.figure(figsize = (25,15))
	#training_indices =((0,1),(2,3),(4,5),(6,7))
	
	for i in range(len(stairs)):
		s = f.add_subplot(1,4,i+1)
		pl.plot(percent_correct[i],'-')
		pl.axhline(0.79,color='k',ls='--')
		sn.despine(offset=10)
		s.set_title('ACC_' + stairs[i], fontsize = 20)
		pl.ylim([.5,1])
		
		# s1 = f.add_subplot(2,4,i+5)
		# pl.plot(stair_values[i], '-')
		# sn.despine(offset=10)
		# s1.set_title('staircase_' + stairs[i], fontsize = 20)
		
 	pl.savefig('data/%s_%d_staircase_plot.pdf'%(initials,run_nr))


