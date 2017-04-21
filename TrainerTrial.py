from __future__ import division
from psychopy import visual, core, misc, event
import numpy#for maths on arrays
from numpy.random import random, shuffle #we only need these two commands from this lib
# from IPython import embed as shell
from math import *
import random, sys
import pandas as pd
import ColorTools as ct

sys.path.append( 'exp_tools' )
# sys.path.append( os.environ['EXPERIMENT_HOME'] )

import Quest

from TrainerStim import *
from Trial import *

class TrainerTrial(Trial):
	def __init__(self, parameters = {}, phase_durations = [], session = None, screen = None, tracker = None):
		super(TrainerTrial, self).__init__(parameters = parameters, phase_durations = phase_durations, session = session, screen = screen, tracker = tracker)
		
		self.stim = TrainerStim(self.screen, self, self.session, parameters = parameters)
		
		this_instruction_string = 'Waiting for scanner to start...'# self.parameters['task_instruction']
		self.instruction = visual.TextStim(self.screen, text = this_instruction_string, font = 'Helvetica Neue', pos = (0, 0), italic = True, height = 30, alignHoriz = 'center')
		self.instruction.setSize((1200,50))

		self.run_time = 0.0
		self.instruct_time = self.t_time = self.fix_time = self.stimulus_time = self.post_stimulus_time = 0.0
		self.instruct_sound_played = False

		self.parameters = parameters.copy()

		if self.session.run_level > 1:

			# Determine trial direction (1 = more yellow, -1 = more blue)
			self.col_trial_direction = 2*round(np.random.rand())-1#np.random.choice([-1,1])	
			if self.parameters[2] > 0:
				if self.session.index_number > 0:
					newSample = self.parameters[5]
				else:
					#self.session.last_sampled_staircase_colr = self.session.last_sampled_staircase_colr ^ 1
					
					#if self.col_trial_direction > 0:
					#	self.staircase_col_index = self.session.standard_parameters['quest_r_index'][1]
					#else:
					self.staircase_col_index = self.session.standard_parameters['quest_r_index']#[0]
					newSample = abs(self.session.staircases[self.staircase_col_index].quantile())
			else:
				if self.session.index_number > 0:
					newSample = -1*self.parameters[5]
				else:
					#self.session.last_sampled_staircase_colg = self.session.last_sampled_staircase_colg ^ 1
					#if self.col_trial_direction > 0:
					#	self.staircase_col_index = self.session.standard_parameters['quest_g_index'][1]
					#else:
					self.staircase_col_index = self.session.standard_parameters['quest_g_index']#[0]
					newSample = -1*abs(self.session.staircases[self.staircase_col_index].quantile())
				


			self.trial_color_value = newSample

			if self.parameters[0] == 45:
				if self.session.index_number > 0:
					newSample = self.parameters[4]
				else:
					#self.session.last_sampled_staircase_ori = self.session.last_sampled_staircase_ori ^ 1
					self.staircase_ori_index = self.session.standard_parameters['quest_o_index']#[0]#[self.session.last_sampled_staircase_ori]
					newSample = abs(self.session.staircases[self.staircase_ori_index].quantile())
			else:
				if self.session.index_number > 0:
					newSample = -1*self.parameters[4]
				else:
					#self.session.last_sampled_staircase_ori = self.session.last_sampled_staircase_ori ^ 1
					self.staircase_ori_index = self.session.standard_parameters['quest_o_index']#[0]#[self.session.last_sampled_staircase_ori]
					newSample = -1*abs(self.session.staircases[self.staircase_ori_index].quantile())
				
			self.ori_trial_direction = 2*round(np.random.rand())-1#np.random.choice([-1,1])			

			self.trial_ori_value = self.ori_trial_direction * newSample	

			self.parameterDict = {'base_ori': self.parameters[0],
									'base_color_lum': self.parameters[1],
									'base_color_a': self.parameters[2],
									'base_color_b': self.parameters[3],
									'stimulus_type': self.parameters[-5],
									'task': self.parameters[-4],
									'trial_orientation': self.trial_ori_value,
									'trial_color': self.trial_color_value,
									'trial_position_x': self.parameters[-2],
									'trial_position_y': self.parameters[-1]																												 																												 
									}			
		else:
			self.parameterDict = {'base_ori': self.parameters[0],
						'base_color_lum': self.parameters[1],
						'base_color_a': self.parameters[2],
						'base_color_b': self.parameters[3],
						'stimulus_type': self.parameters[-5],
						'task': self.parameters[-4],
						'trial_position_x': self.parameters[-2],
						'trial_position_y': self.parameters[-1]																												 																												 
						}
	
		self.stim.make_stimulus()
		

	
	def draw(self):
		"""docstring for draw"""
		if self.phase == 0: # ITI

			self.session.fixation.color = (1,1,1)

			self.session.fixation_outer_rim.draw()
			self.session.fixation_rim.draw()
			self.session.fixation.draw()
			
			#self.session.show_stim_demo(True)
		
		elif (self.phase == 1) and (self.session.run_level>0): # Audio cue
			self.session.fixation_outer_rim.draw()
			self.session.fixation_rim.draw()
			self.session.fixation.draw()
			
			#self.session.show_stim_demo(False)

			if not self.instruct_sound_played:
				self.stim.play_cue_sound()
				self.instruct_sound_played = True

		elif (self.phase == 2) and (self.session.run_level>0): # Cue-stim interval
			
			self.session.fixation_outer_rim.draw()
			self.session.fixation_rim.draw()
			self.session.fixation.draw()
			
			self.session.show_stim_demo(False)
		
			#self.stim.draw(self.phase)
			
			#evemtwaitKeys(keyList=self.session.standard_parameters['trainer_response_buttons'])

		elif self.phase == 3: # Show first stimulus
			self.session.fixation_outer_rim.draw()
			self.session.fixation_rim.draw()			
			self.session.fixation.draw()																												 

			if (self.session.run_level==0) and (not self.instruct_sound_played):
				self.stim.play_cue_sound()
				self.instruct_sound_played = True

			self.stim.draw(self.phase)
			# self.phase_redraw = False

		super(TrainerTrial, self).draw( )

	def event(self):
		for ev in event.getKeys():
			if len(ev) > 0:
				if ev in ['esc', 'escape', 'q']:
					self.events.append([-99,self.session.clock.getTime()-self.start_time])
					self.stopped = True
					self.session.stopped = True
					print 'run canceled by user'
				# it handles both numeric and lettering modes 
				elif ev == ' ':
					self.events.append([0,self.session.clock.getTime()-self.start_time])
					if self.phase == 0:
						self.phase_forward()
					else:
						self.events.append([-99,self.session.clock.getTime()-self.start_time])
						# super(ExpectationTrial, self).key_event( ev )
						self.stopped = True
						print 'trial canceled by user'
				elif ev == 't': # TR pulse
					self.events.append([99,self.session.clock.getTime()-self.start_time])
					# super(ExpectationTrial, self).key_event( ev )
					if (self.phase == 0) + (self.phase==2):
						self.phase_forward()
				elif ev in self.session.standard_parameters['trainer_response_buttons']:
					# first check, do we even need an answer?
					if self.phase == self.session.standard_parameters['trainer_response_phase']:

						super(TrainerTrial, self).key_event( ev )

						response = -1

						print 'Cue: %d, response: %d (%s)' % (self.parameters[self.session.standard_parameters['cue_index_level_0']],self.session.standard_parameters['trainer_response_buttons'].index(ev), ev)

						if self.parameters[self.session.standard_parameters['cue_index_level_0']] == self.session.standard_parameters['trainer_response_buttons'].index(ev):
							self.session.correct_responses += 1
						
						self.phase_forward()
						

				#event_msg = 'trial ' + str(self.ID) + ' key: ' + str(ev) + ' at time: ' + str(self.session.clock.getTime())
				#self.events.append(event_msg)
		
			

	def run(self, ID = 0):
		self.ID = ID
		super(TrainerTrial, self).run()
				
		while not self.stopped:
			self.run_time = self.session.clock.getTime() - self.start_time

			# events and draw
			self.event()
			self.draw()
			
			if (self.phase==0) and (self.session.clock.getTime()-self.start_time >= self.phase_durations[0]):
				self.phase_forward()
			
			if (self.phase>0) and (self.session.clock.getTime()-self.phase_start_time >= self.phase_durations[self.phase]):
				self.phase_forward()
			
			# if (self.phase==0) and (self.run_time >= np.sum(self.phase_durations[0:(self.phase+1)])):
				# print 'on to the next phase'
				# self.phase_forward()
				
			# if (self.phase==1) and (self.run_time >= np.sum(self.phase_durations[0:(self.phase+1)])):
				# print 'on to the next phase'
				# self.phase_forward()				

			# if (self.phase==2) and (self.run_time >= np.sum(self.phase_durations[0:(self.phase+1)])):
				# print 'on to the next phase'
				# self.phase_forward()				
				
			# if (self.phase==3) and (self.run_time >= np.sum(self.phase_durations[0:(self.phase+1)])):
				# print 'on to the next phase'
				# self.phase_forward()

			if self.phase == len(self.phase_durations):
					self.stopped = True
		

	
		self.stop()
		
	def stop(self):
		super(TrainerTrial, self).stop()
		
		# self.session.pdOutput.append(pd.DataFrame(self.parameterDict, index = [self.ID]))
		