import numpy as np

# standard parameters
standard_parameters = {
	
	## common parameters:
	'TR':               	 1,#0.945,		# VERY IMPORTANT TO FILL IN!! (in secs)
	# 'number_of_quest_trials':  120,		# this needs to divide into 8
	# 'number_of_trials':       400,		# this needs to divide into 8
	'ntrials_per_stim':		 25,#100,   # this * 16 will be the total number of trials
	#'mapper_ntrials':		       168,
	#'mapper_max_index': 63,
	
	## stimulus parameters:calc
	'stimulus_size': 2.0,#1.5,	# diameter in dva

	'stimulus_positions': ([2.5, 2.5], [2.5, -2.5], [-2.5, -2.5], [-2.5, 2.5],[2.5, 2.5],[-2.5, 2.5],[-2.5, -2.5], [2.5, -2.5]),#(0.0, 0.0),

	'stimulus_base_spatfreq': 0.04,#0.04,

	'stimulus_base_orientation': (45, 135),#(0,90),#
	'stimulus_base_colors': ((55,80,75), (55,-80,75)),

	'quest_initial_stim_values': (70, 70, 3, 3),

	'quest_stepsize': [15,15,1,1],
				 
	'quest_r_index': (0),#(0,1),
	'quest_g_index': (1),#(2,3),
	'quest_h_index': (2),#(4,5),
	'quest_v_index': (3),
	
	'quest_max_vals': [110,110,15,15],

	'session_types': [0,1,2,3],
	'tasks': [1,2],

	## timing of the presentation:

	'timing_start_empty': 15,
	'timing_finish_empty': 15,


	'timing_stim_1_Duration' : .15, # duration of stimulus presentation, in sec
	'timing_ISI'             : .03,
	'timing_stim_2_Duration' : .15, # duration of stimulus presentation, in sec
	# 'timing_preStimDuration' : 0.75, # SOA will be random between 1 frame and this
	'timing_cue_duration'    : 1.0,	# Duration for each cue separately
	'timing_stimcue_interval' : 0.5,
	'timing_responseDuration' : 3.0, # time to respond	
	'timing_ITI_duration':  (0.5, 1.5),		# in sec

	'response_buttons_right': ['j','l'],#['b','y'],
	'response_buttons_left': ['s','f'],#['w','e'],

	'response_buttons_orientation': [],
	'response_buttons_color': [],

	'main_task_instruction': 'Experiment phase. \n\n\n You should by now have a good idea of what sound matches to each stimulus. This is important for the experiment, so if you are unsure please do the training again! \n\n\n The experimentator will instruct you on how to do this task. \n\n Make sure to be accurate but also try to respond as fast as possible! \n\n Press spacebar when you are ready to begin!',


	############
	## TRAINING PARAMETERS
	############

	####
	## LEVEL 0
	####

	'demo_stim_pos_x': [-3.0, -1.0, 1.0, 3.0],
	'demo_stim_pos_y': [3.0, 3.0, 3.0, 3.0],	
	
	'trainer_first_level_repeats': 4,

	'trainer_level_0_task_instruction': 'Learning phase.',
	'trainer_level_1_task_instruction': 'Learning phase: test.',

	'cue_index_level_0': -3,
	'task_index_level_0': 0,

	## timing of the presentation:
	'trainer_level_0_timing_stim_1_Duration' : 0.5, # duration of stimulus presentation, in sec
	'trainer_level_0_timing_cue_duration'    : 0.0,	# Duration for each cue separately	
	'trainer_level_0_timing_responseDuration' : 0.0, # time to respond	
	'trainer_level_1_timing_cue_duration'    : 0.5,	# Duration for each cue separately	
	'trainer_level_1_timing_responseDuration' : 15.0, # time to respond		
	'trainer_level_0_timing_ITI_duration':  (0.5, 0.75),		# in sec
	'trainer_response_buttons': ['1','2','8','9'], 
	'trainer_response_phase': 2
}

# response_button_signs = {
# 'e':-1,  # left 'less' answer
# 'b':1,   # right 'more' answer
# 'y':2}   # confirm color match

# response_buttons = {
# 	'c' : -1, # more yellow's'
# 	'e' : 1, # more blue'f'
# 	'b' : -1, # CCW  more vertical'j'
# 	'y' : 1 # CW    more horizontal 'l'
# }

# response_buttons = {
# 	'w' : -1, # more yellow's'
# 	'e' : 1, # more blue'f'
# 	'b' : -1, # CCW  more vertical'j'
# 	'y' : 1 # CW    more horizontal 'l'
# }

screen_res = (1024,768)#(1680,1050)#(3840,2160)#(1920,1080)
screen_dist = 65.0
screen_size = (33.8,27.1)#(33.8,27.1)
background_color = (0.0, 0.0, 0.0)

screen_num = -1#0#1
# screen_res = (1024,768)#(1680,1050)#(1920,1080)#(2560,1440)#(3840,2160)#(1920,1080)#(1280,1024)#(3840,2160)#(1920,1080)#(
# screen_dist = 60#225#60#225#60.0 # 159.0
# screen_size = (33.8,27.1)#(48, 38) #(69.84,39.29)# (70, 40)
screen_full = False
# background_color = (0.0, 0.0, 0.0)