from __future__ import division
from psychopy import visual, core, misc, event, filters
import numpy as np
from scipy.signal import convolve2d
from IPython import embed as dbstop
from math import *
import random, sys, pyaudio, wave
import colorsys
import ColorTools as ct

sys.path.append( 'exp_tools' )
# sys.path.append( os.environ['EXPERIMENT_HOME'] )


class ExpectationStim(object):
	def __init__(self, screen, trial, session, parameters):
		# parameters
		
		self.trial = trial
		self.session = session
		self.screen = screen
		self.trial_settings = parameters.copy()
		self.size_pix = session.standard_parameters['stimulus_size'] * session.pixels_per_degree
		

		self.phase = 0

		self.setup_cue() 

		self.pyaudio = pyaudio.PyAudio()

		self.timer = core.Clock()

		#self.make_stimulus()
		self.setup_cue()
		
		self.printcolor = True

	def make_stimulus(self):

		self.stimulus = visual.GratingStim(self.screen, tex = 'sin', mask = 'raisedCos', maskParams = {'fringeWidth': 0.6}, texRes = 1024, sf = self.session.standard_parameters['stimulus_base_spatfreq'], ori = self.trial_settings['base_ori'], units = 'pix',  size = (self.size_pix, self.size_pix), pos = (self.trial_settings['trial_position_x']*self.session.pixels_per_degree, self.trial_settings['trial_position_y']*self.session.pixels_per_degree), colorSpace = 'rgb', color = ct.lab2psycho([self.trial_settings['base_color_lum'], self.trial_settings['base_color_a'], self.trial_settings['base_color_b']]))
		#self.stimulus = visual.GratingStim(self.screen, tex = 'sin', mask = 'raisedCos', maskParams = {'fringeWidth': 0.6}, texRes = 1024, sf = self.session.standard_parameters['stimulus_base_spatfreq'], ori = self.trial_settings['base_ori'], units = 'deg',  size = (self.size_pix, self.size_pix), pos = (self.trial_settings['trial_position_x'], self.trial_settings['trial_position_y']), colorSpace = 'rgb', color = ct.lab2psycho([self.trial_settings['base_color_lum'], self.trial_settings['base_color_a'], self.trial_settings['base_color_b']]))
		#self.stimulus2 = visual.GratingStim(self.screen, tex = 'sin', mask = 'raisedCos', maskParams = {'fringeWidth': 0.6}, texRes = 1024, sf = self.session.standard_parameters['stimulus_base_spatfreq'], ori = self.trial_settings[0] + self.trial.trial_ori_value,  size = (self.size_pix, self.size_pix), pos = (self.trial_settings[-2], self.trial_settings[-1]), colorSpace = 'rgb', color = ct.lab2psycho([self.trial_settings[1], self.trial_settings[2] + self.trial.trial_color_value, self.trial_settings[3]]))
		
	def update_stimulus(self):
		#pass	
		self.stimulus.ori = self.trial_settings['base_ori'] + self.trial.trial_ori_value
		if self.trial.col_trial_direction > 0:
			#print [self.trial_settings[1], self.trial_settings[2], self.trial_settings[3] - abs(self.trial.trial_color_value)
					
			self.stimulus.color = ct.lab2psycho([self.trial_settings['base_color_lum'], self.trial_settings['base_color_a'], self.trial_settings['base_color_b'] - abs(self.trial.trial_color_value)])
		else:
			self.stimulus.color = ct.lab2psycho([self.trial_settings['base_color_lum'], self.trial_settings['base_color_a'] - self.trial.trial_color_value, self.trial_settings['base_color_b']])

	def play_warning_sound(self):
		
		# assuming 44100 Hz, mono channel np.int16 format for the sounds
		stream_data = self.parameters['sounds']['error']
		
		self.frame_counter = 0
		def callback(in_data, frame_count, time_info, status):
 			data = stream_data[self.frame_counter:self.frame_counter+frame_count]
 			self.frame_counter += frame_count
 			return (data, pyaudio.paContinue)

		# open stream using callback (3)
		stream = self.pyaudio.open(format=pyaudio.paInt16,
						channels=1,
						rate=44100,
						output=True,
						stream_callback=callback)

		stream.start_stream()
		# stream.write(stream_data)	
		#stream_data = None


	def setup_cue(self):

		# if self.trial_settings['cue_stimulus'] == 0:
			# self.cue_sound = 'red45'
		# elif self.trial_settings[-5] == 1:
			# self.cue_sound = 'red135'
		# elif self.trial_settings[-5] == 2:
			# self.cue_sound = 'green45'
		# elif self.trial_settings[-5] == 3:
			# self.cue_sound = 'green135'

		self.cue_sound = self.trial_settings['trial_cue']

		if self.trial_settings['task'] == 1:
			taskMessage = 'K'
		else:
			taskMessage = 'O'

			#original height of K/O = .37 || if necessary, change to .74
	 	self.task_stim = visual.TextStim(self.screen, text = taskMessage, color = 'black', bold = True, pos = (0.0,0.0), height = 0.37 * self.session.pixels_per_degree)			
		self.response_stim = visual.TextStim(self.screen, text = '?', color = 'black', bold = True, pos = (0.0,0.0), height = 0.4 * self.session.pixels_per_degree)				 	

		#self.pointer = visual.Line(self.screen, start = (np.sign(self.trial_settings['trial_position_x']) * 0.25 * self.session.pixels_per_degree, np.sign(self.trial_settings['trial_position_y']) * 0.25 * self.session.pixels_per_degree), end = (self.session.pixels_per_degree*self.trial_settings['trial_position_x']/3.0, self.session.pixels_per_degree*self.trial_settings['trial_position_y']/3.0))

	def play_cue_sound(self):
		
		# assuming 44100 Hz, mono channel np.int16 format for the sound


		stream_data = self.session.sounds[self.cue_sound]
		

		self.frame_counter = 0
		def callback(in_data, frame_count, time_info, status):
 			data = stream_data[self.frame_counter:self.frame_counter+frame_count]
 			self.frame_counter += frame_count
 			return (data, pyaudio.paContinue)

		# open stream using callback (3)
		stream = self.pyaudio.open(format=pyaudio.paInt16,
						channels=1,
						rate=44100,
						output=True,
						stream_callback=callback)

		stream.start_stream()	
		
		del stream

	
	def draw(self, phase = 0):
		self.phase = phase		
		
		if (self.phase >= 2) and (self.phase < 4):
			self.task_stim.draw()
			#self.pointer.draw()

		if self.phase == 4:
			self.stimulus.draw()
			# if self.printcolor:
				# print self.stimulus.color
				# self.printcolor = False

		if self.phase == 6:
			self.stimulus.draw()
			# if self.printcolor:
				# print self.stimulus.color
				# self.printcolor = False
		if self.phase >= 7:
			self.response_stim.draw()
		# log_msg = 'stimulus draw for phase %f, at %f'%(phase, self.session.clock.getTime())
		# self.trial.events.append( log_msg )
		# if self.session.tracker:
		# 	self.session.tracker.log( log_msg )			
		
