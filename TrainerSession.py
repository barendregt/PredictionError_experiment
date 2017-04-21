from __future__ import division
from psychopy import visual, core, misc, event
import numpy as np
from IPython import embed as dbstop
from math import *

import os, sys, time, datetime, cPickle
import pygame
from pygame.locals import *
# from pygame import mixer, time



sys.path.append( 'exp_tools' )
# sys.path.append( os.environ['EXPERIMENT_HOME'] )


import Quest
from Session import *
from TrainerTrial import *
from standard_parameters import *
# from Staircase import YesNoStaircase

# import appnope
# appnope.nope()

class TrainerSession(EyelinkSession):
	def __init__(self, subject_initials, index_number,scanner='n', tracker_on=0, task=()):
		super(TrainerSession, self).__init__( subject_initials, index_number)

		self.create_screen( size = screen_res, full_screen = 0, physical_screen_distance = 159.0, background_color = background_color, physical_screen_size = (70, 40) )

		self.create_output_file_name()
		
		self.create_tracker(tracker_on = False)

		self.response_buttons = response_buttons

		self.setup_sounds()

		self.fileOperations = {}
		
		self.run_level = 0#index_number

		self.standard_parameters = standard_parameters

		self.pdOutput = list()
		# trials can be set up independently of the staircases that support their parameters
		
		self.parameter_names = ['base_ori', 'base_r', 'base_g', 'base_b', 'ori_offset', 'color_offset', 'stim_type', 'task', 'x', 'y']

		#exec('self.prepare_trials_' + str(self.run_level) + '()')
		self.prepare_trials()
		
	def create_output_file_name(self, data_directory = 'data'):
		"""create output file"""
		now = datetime.datetime.now()
		opfn = now.strftime("%Y-%m-%d_%H.%M.%S")
		
		if not os.path.isdir(data_directory):
			os.mkdir(data_directory)
			
		#self.output_file = os.path.join(data_directory, self.subject_initials + '_' + str(self.index_number) + '_' + opfn )
		self.output_file = os.path.join(data_directory, self.subject_initials + '_t' + str(self.index_number))# + '_' + opfn )
	
	def setup_sounds(self):
		"""initialize pyaudio backend, and create dictionary of sounds."""
		self.pyaudio = pyaudio.PyAudio()

		task_sounds = [['lowToneSingle.wav','lowToneDouble.wav','highToneSingle.wav','highToneDouble.wav'],
				   ['highToneSingle.wav','highToneDouble.wav','lowToneSingle.wav','lowToneDouble.wav'],
				   ['lowToneSingle.wav','highToneSingle.wav','lowToneDouble.wav','highToneDouble.wav'],
				   ['lowToneDouble.wav','highToneDouble.wav','lowToneSingle.wav','highToneSingle.wav'],
				   ['lowToneDouble.wav','lowToneSingle.wav','highToneDouble.wav','highToneSingle.wav'],
				   ['highToneDouble.wav','highToneSingle.wav','lowToneDouble.wav','lowToneSingle.wav'],
				   ['highToneSingle.wav','lowToneSingle.wav','highToneDouble.wav','lowToneDouble.wav'],
				   ['highToneDouble.wav','lowToneDouble.wav','highToneSingle.wav','lowToneSingle.wav']					   
					  ]

		if not os.path.isfile(os.path.join('data', self.subject_initials + '_soundmap.txt')):
			f = open(os.path.join('data', self.subject_initials + '_soundmap.txt'),'w')			

			f.write(','.join(task_sounds[np.random.randint(len(task_sounds))]))
			f.close()

		f = open(os.path.join('data', self.subject_initials + '_soundmap.txt'),'r')

		sub_task_sounds = f.read().split(",")

		self.sound_files = {
						   'red45' : 'sounds/' + sub_task_sounds[0],
						   'red135' : 'sounds/' + sub_task_sounds[1],
						   'green45' : 'sounds/' + sub_task_sounds[2],
						   'green135' : 'sounds/' + sub_task_sounds[3]
						   }
		self.sounds = {}
		for sf in self.sound_files:
			self.read_sound_file(file_name = self.sound_files[sf], sound_name = sf)
		# print self.sounds		
		
	
	def prepare_trials(self):
		"""docstring for prepare_trials(self):"""

		# self.standard_parameters = standard_parameters

		trial_params = list()


		# trial_types = np.vstack([[a, b[0], b[1], b[2]] for a in self.params['stimulus_base_orientation'] for b in zip(self.params['stimulus_base_color_r'], self.params['stimulus_base_color_g'], self.params['stimulus_base_color_b'])])
		trial_types = np.vstack([[[a,b[0], b[1], b[2]] for a in self.standard_parameters['stimulus_base_orientation']] for b in self.standard_parameters['stimulus_base_colors']])		

		for ii in range(0,4):
			trial_params.extend(np.hstack([np.tile(trial_types[ii],(self.standard_parameters['trainer_first_level_repeats'],1)), np.zeros((self.standard_parameters['trainer_first_level_repeats'],2)), np.zeros((self.standard_parameters['trainer_first_level_repeats'],2)), ii*np.ones((self.standard_parameters['trainer_first_level_repeats'],2))]))


		trial_params1 = np.vstack([trial_params, trial_params, trial_params])
		
		self.trainer_level_up = len(trial_params1)
		
		trial_params2 = np.array(trial_params)
		np.random.shuffle(trial_params2)
		trial_params = np.vstack([trial_params1, trial_params2])
		
		self.correct_responses = 0

		self.trial_array = np.hstack([trial_params, np.tile([0,0],(len(trial_params),1))])

		sub_sounds = [s.split(".wav")[0] for s in open(os.path.join('data', self.subject_initials + '_soundmap.txt'),'r').read().split(",")]
		
		#Prepare demo stimuli
		self.demo_stim = list()
		self.demo_key = list()
		self.demo_sound = list()
		for ii,tt in enumerate(trial_types):
			self.demo_stim.append(visual.GratingStim(self.screen, tex = 'sin', mask = 'raisedCos', maskParams = {'fringeWidth': 0.6}, texRes = 1024, sf = self.standard_parameters['stimulus_base_spatfreq'], ori = tt[0], units = 'pix',  size = (self.standard_parameters['stimulus_size']*self.pixels_per_degree, self.standard_parameters['stimulus_size']*self.pixels_per_degree), pos = (self.standard_parameters['demo_stim_pos_x'][ii]*self.pixels_per_degree, self.standard_parameters['demo_stim_pos_y'][ii]*self.pixels_per_degree), colorSpace = 'rgb', color = ct.lab2psycho([tt[1],tt[2],tt[3]])))
			self.demo_key.append(visual.TextStim(self.screen, text = '(' + self.standard_parameters['trainer_response_buttons'][ii] + ')', font = 'Helvetica Neue', pos = (self.standard_parameters['demo_stim_pos_x'][ii]*self.pixels_per_degree, self.standard_parameters['demo_stim_pos_y'][ii]*self.pixels_per_degree - 1.5*self.pixels_per_degree), italic = True, height = 18))
			self.demo_sound.append(visual.TextStim(self.screen, text = sub_sounds[ii], font = 'Helvetica Neue', pos = (self.standard_parameters['demo_stim_pos_x'][ii]*self.pixels_per_degree, self.standard_parameters['demo_stim_pos_y'][ii]*self.pixels_per_degree - 1.5*self.pixels_per_degree), italic = True, height = 11))			
	

	# def prepare_trials_1(self):
		# """docstring for prepare_trials(self):"""

		#self.standard_parameters = standard_parameters

		# trial_params = list()


		#trial_types = np.vstack([[a, b[0], b[1], b[2]] for a in self.params['stimulus_base_orientation'] for b in zip(self.params['stimulus_base_color_r'], self.params['stimulus_base_color_g'], self.params['stimulus_base_color_b'])])
		# trial_types = np.vstack([[[a,b[0], b[1], b[2]] for a in self.standard_parameters['stimulus_base_orientation']] for b in self.standard_parameters['stimulus_base_colors']])

		# for ii in range(0,4):
			# trial_params.extend(np.hstack([np.tile(trial_types[ii],(self.standard_parameters['trainer_second_level_repeats'],1)), np.zeros((self.standard_parameters['trainer_second_level_repeats'],2)), np.zeros((self.standard_parameters['trainer_second_level_repeats'],2)), ii*np.ones((self.standard_parameters['trainer_second_level_repeats'],2))]))


		# trial_params = np.array(trial_params)

		# trial_params = trial_params[np.random.permutation(len(trial_params))]

		# self.trial_array = np.hstack([trial_params, np.tile(self.standard_parameters['stimulus_position'],(len(trial_params),1))])
		
		# self.correct_responses = 0

		#Prepare demo stimuli
		# self.demo_stim = list()
		# self.demo_key = list()
		# for ii,tt in enumerate(trial_types):
			# self.demo_stim.append(visual.GratingStim(self.screen, tex = 'sin', mask = 'raisedCos', maskParams = {'fringeWidth': 0.6}, texRes = 1024, sf = self.standard_parameters['stimulus_base_spatfreq'], ori = tt[0], units = 'pix',  size = (self.standard_parameters['stimulus_size']*self.pixels_per_degree, self.standard_parameters['stimulus_size']*self.pixels_per_degree), pos = (self.standard_parameters['demo_stim_pos_x'][ii]*self.pixels_per_degree, self.standard_parameters['demo_stim_pos_y'][ii]*self.pixels_per_degree), colorSpace = 'rgb', color = ct.lab2psycho([tt[1],tt[2],tt[3]])))
			# self.demo_key.append(visual.TextStim(self.screen, text = '(' + self.standard_parameters['trainer_response_buttons'][ii] + ')', font = 'Helvetica Neue', pos = (self.standard_parameters['demo_stim_pos_x'][ii]*self.pixels_per_degree, self.standard_parameters['demo_stim_pos_y'][ii]*self.pixels_per_degree - 1.5*self.pixels_per_degree), italic = True, height = 30))
	
	def show_stim_demo(self, hideKeys = False, hideSounds = True):
		for t,s,snd in zip(self.demo_key, self.demo_stim, self.demo_sound):
			s.draw()
			if not hideKeys:
				t.draw()
			if not hideSounds:
				snd.draw()
		
	
	def close(self):
		
		pc = 100 * (self.correct_responses / (len(self.trial_array)/4))
		
		print('You scored %d percent correct on the task' % (pc))
	
		this_instruction_string = 'You scored %d percent correct on the task' % (pc)
		self.instruction = visual.TextStim(self.screen, text = this_instruction_string, font = 'Helvetica Neue', pos = (0, 0), italic = True, height = 20, alignHoriz = 'center')
		#self.instruction.setSize((1200,50))
		self.instruction.draw()

		self.screen.flip()

		event.waitKeys()		

		super(TrainerSession, self).close()
	
	def run(self):
		"""docstring for fname"""
		# cycle through trials


	

		# fixation point
		self.fixation_rim = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=0.5 * self.pixels_per_degree, pos = np.array((0.0,0.0)), color = (-1.0, -1.0, -1.0), maskParams = {'fringeWidth':0.4})
		self.fixation_outer_rim = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=0.5 * self.pixels_per_degree, pos = np.array((0.0,0.0)), color = (-1.0, -1.0, -1.0), maskParams = {'fringeWidth':0.4})
		self.fixation = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=0.48 * self.pixels_per_degree, pos = np.array((0.0,0.0)), color = (1.0, 1.0, 1.0), opacity = 1.0, maskParams = {'fringeWidth':0.4})

		# Wait to start the experiment
		self.fixation_outer_rim.draw()
		self.fixation_rim.draw()
		self.fixation.draw()

		# this_instruction_string = self.standard_parameters['trainer_level_0_task_instruction']
		# self.instruction = visual.TextStim(self.screen, text = this_instruction_string, font = 'Helvetica Neue', pos = (-50.0, -200.0), height = 16, wrapWidth=1000)
		#self.instruction.setSize((2000,2000))
		# self.instruction.draw()


		self.show_stim_demo(hideKeys = True, hideSounds = False)

		self.screen.flip()

		event.waitKeys(keyList = ['space'])

		event.clearEvents()

		rStart = 0	
		#self.trainer_level_up = 2
		for self.trialID in range(rStart, len(self.trial_array)):
		
			if self.trialID == self.trainer_level_up:
				self.run_level = 1
				
				# Wait to start th experiment
				self.fixation_outer_rim.draw()
				self.fixation_rim.draw()
				self.fixation.draw()

				this_instruction_string = self.standard_parameters['trainer_level_1_task_instruction']
				self.instruction = visual.TextStim(self.screen, text = this_instruction_string, font = 'Helvetica Neue', pos = (-50.0, -200.0), height = 12, wrapWidth=1000)
				# self.instruction.setSize((1200,50))
				self.instruction.draw()


				self.show_stim_demo(hideKeys = False)

				self.screen.flip()

				event.waitKeys(keyList = ['space'])			
		
			# prepare the parameters of the following trial based on the shuffled trial array
			this_trial_parameters = self.trial_array[self.trialID,:]			

			# print 'Running trial ' + str(self.trialID)
			
			self.phase_durations = np.array([
				self.standard_parameters['trainer_level_0_timing_ITI_duration'], 	# inter trial interval
				self.standard_parameters['trainer_level_' + str(self.run_level) + '_timing_cue_duration'],	# present second cue (audio)
				self.standard_parameters['trainer_level_' + str(self.run_level) + '_timing_responseDuration'],# wait before presenting stimulus
				self.standard_parameters['trainer_level_0_timing_stim_1_Duration']		
				])	# ITI			

			these_phase_durations = self.phase_durations.copy()
			these_phase_durations[0] = these_phase_durations[0][0] + np.random.rand()*these_phase_durations[0][1]
			
			this_trial = TrainerTrial(this_trial_parameters, phase_durations = these_phase_durations, session = self, screen = self.screen, tracker = self.tracker)
			
			# run the prepared trial
			this_trial.run(ID = self.trialID)
			
			
			
			# if self.index_number > 0:
			# 	self.partial_store(self.trialID)			
			
			if self.stopped == True:
				break
			
		self.close()
	

