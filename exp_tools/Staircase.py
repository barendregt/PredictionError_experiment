#!/usr/bin/env python
# encoding: utf-8
"""
Staircase.py

Created by Tomas HJ Knapen on 2009-11-26.
Copyright (c) 2009 TK. All rights reserved.
"""


import os, sys, datetime
import subprocess, logging
import pickle, datetime, time

import scipy as sp
import numpy as np
# import matplotlib.pylab as pl
from math import *

class OneUpOneDownStaircase(object):
	"""
	OneUpOneDownStaircase object, for one-up-one-down staircase in its standard form.
	"""
	def __init__(self, initial_value, initial_stepsize, nr_reversals = 10, increment_value = None, stepsize_multiplication_on_reversal = 0.75, max_nr_trials = 40 , min_test_val = None, max_test_val = None):
		self.initial_value = initial_value
		self.initial_stepsize = initial_stepsize
		self.nr_reversals = nr_reversals
		self.increment_value = initial_stepsize#increment_value
		self.stepsize_multiplication_on_reversal = stepsize_multiplication_on_reversal
		self.max_nr_trials = max_nr_trials

		self.min_test_val = min_test_val
		self.max_test_val = max_test_val
		
		self.test_values = [self.initial_value] # keep a log of test values
		self.present_increment_value = initial_stepsize#increment_value
		
		# set up filler variables
		self.past_answers = []
		self.nr_trials = 0
		self.nr_correct = 0
		self.present_nr_reversals = 0
	
	# def test_value(self):
	# 	return self.test_value
	
	def get_intensity(self):
		return self.test_values[-1]

	def increase_difficulty(self):

		if self.min_test_val is not None:
			self.test_values.append(max([self.test_values[-1] - self.present_increment_value, self.min_test_val]))
		else:
			self.test_values.append(self.test_values[-1] - self.present_increment_value)


	def decrease_difficulty(self):

		if self.max_test_val is not None:
			self.test_values.append(min([self.test_values[-1] + self.present_increment_value, self.max_test_val]))
		else:
			self.test_values.append(self.test_values[-1] + self.present_increment_value)		

	def answer( self, correct ):
		continue_after_this_trial = True
		self.nr_trials = self.nr_trials + 1
		if correct: # answer was correct and so we lower the contrast/whatever value
			self.increase_difficulty()#self.test_value = self.test_value - self.present_increment_value
		else:
			self.decrease_difficulty()#self.test_value = self.test_value + self.present_increment_value
	
		self.past_answers.append(correct)
			
		if self.nr_trials > 1:
			if self.past_answers[-1] != self.past_answers[-2]:	# we have a reversal here
				self.present_nr_reversals = self.present_nr_reversals + 1
				if self.present_nr_reversals % 2 == 0:
					self.present_increment_value = self.present_increment_value * self.stepsize_multiplication_on_reversal
				if self.present_nr_reversals >= self.nr_reversals:
					continue_after_this_trial = False
			else: 
				pass
			if self.nr_trials >= self.max_nr_trials:
				continue_after_this_trial = False
		
		return continue_after_this_trial
	
class TwoUpOneDownStaircase(OneUpOneDownStaircase):
	def __init__(self, initial_value, initial_stepsize, nr_reversals = 10, increment_value = None, stepsize_multiplication_on_reversal = 0.75, max_nr_trials = 40, min_test_val = None, max_test_val = None ):
		super(TwoUpOneDownStaircase, self).__init__(initial_value, initial_stepsize, nr_reversals, increment_value, stepsize_multiplication_on_reversal, max_nr_trials, min_test_val, max_test_val)
		self.past_answers = []# [0.5, 0.5, 0.5]
	
	def answer( self, correct ):
		continue_after_this_trial = True
		self.nr_trials = self.nr_trials + 1
		self.past_answers.append(correct)

		if correct:
		
			#nr_corrects_in_last_2_trials = np.array(self.past_answers, dtype = float)[-2:].sum()
			self.nr_correct += 1
		
			if self.nr_correct == 2:	# this subject is too good for this stimulus value
				self.increase_difficulty() #self.test_value = self.test_value - self.present_increment_value
				self.nr_correct = 0
		else:
			self.decrease_difficulty()#self.test_value = self.test_value + self.present_increment_value
			self.nr_correct = 0
		
		if self.nr_trials > 1:
			if self.past_answers[-1] != self.past_answers[-2]:	# we have a reversal here
				self.present_nr_reversals = self.present_nr_reversals + 1
				if self.present_nr_reversals % 2 == 0:
					self.present_increment_value = self.present_increment_value * self.stepsize_multiplication_on_reversal
				if self.present_nr_reversals >= self.nr_reversals:
					continue_after_this_trial = False
			else: 
				pass
			# if self.nr_trials >= self.max_nr_trials:
			# 	continue_after_this_trial = False
		
		return continue_after_this_trial
	
class ThreeUpOneDownStaircase(TwoUpOneDownStaircase):
	def answer( self, correct ):
		continue_after_this_trial = True
		self.nr_trials = self.nr_trials + 1
		self.past_answers.append(correct)
		
		if correct:

			#nr_corrects_in_last_3_trials = np.array(self.past_answers, dtype = float)[-3:].sum()
			self.nr_correct += 1

			if self.nr_correct == 3:	# this subject is too good for this stimulus value
				self.increase_difficulty()#self.test_value = self.test_value - self.present_increment_value
				self.nr_correct = 0

		else:
			self.decrease_difficulty()#self.test_value = self.test_value + self.present_increment_value
			self.nr_correct = 0
		
		if self.nr_trials > 1:
			if self.past_answers[-1] != self.past_answers[-2]:	# we have a reversal here
				self.present_nr_reversals = self.present_nr_reversals + 1
				if self.present_nr_reversals % 2 == 0:
					self.present_increment_value = self.present_increment_value * self.stepsize_multiplication_on_reversal
				if self.present_nr_reversals >= self.nr_reversals:
					continue_after_this_trial = False
			else: 
				pass
			#if self.nr_trials >= self.max_nr_trials:
			#	continue_after_this_trial = False
		
		return continue_after_this_trial
	
class YesNoStaircase(object):
	def __init__(self, initial_value, initial_stepsize, nr_reversals = 100, stepsize_multiplication_on_reversal = 0.75, max_nr_trials = 400 ):
		self.initial_value = initial_value
		self.initial_stepsize = initial_stepsize
		self.nr_reversals = nr_reversals
		self.stepsize_multiplication_on_reversal = stepsize_multiplication_on_reversal
		self.max_nr_trials = max_nr_trials
		
		self.test_value = self.initial_value
		self.present_increment_value = initial_stepsize
		
		# set up filler variables
		self.past_answers = []
		self.nr_trials = 0
		self.present_nr_reversals = 0
	
	def test_value(self):
		return self.test_value
	
	def answer( self, correct ):
		continue_after_this_trial = True
		self.nr_trials = self.nr_trials + 1
		if correct: # answer was correct and so we lower the contrast/whatever value according to Kaernbach's method
			self.test_value = self.test_value - self.present_increment_value
		else:
			self.test_value = self.test_value + 3.0 * self.present_increment_value
	
		self.past_answers.append(correct)
			
		if self.nr_trials > 1:
			if self.past_answers[-1] != self.past_answers[-2]:	# we have a reversal here
				self.present_nr_reversals = self.present_nr_reversals + 1
				if self.present_nr_reversals % 2 == 0:
					self.present_increment_value = self.present_increment_value * self.stepsize_multiplication_on_reversal
				if self.present_nr_reversals >= self.nr_reversals:
					continue_after_this_trial = False
			else: 
				pass
			if self.nr_trials >= self.max_nr_trials:
				continue_after_this_trial = False
		
		return continue_after_this_trial
	
	