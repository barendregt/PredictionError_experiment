import sys, datetime
# from Tkinter import *

from IPython import embed

sys.path.append( 'exp_tools' )

from ExpectationSession import *

from TrainerSession import *

from plot_staircases import plot_staircases

# useTracker = True

def main():
	initials = raw_input('Subject initials: ')

	training = raw_input('Training? (y/n): ')
	task = (1,2)
	run_nr = 0
	if training == 'n':
		run_nr = int(raw_input('Run number: '))

		multi_task = raw_input('Multi task (y/n)?: ')

		if multi_task == 'n':
			task = [int(raw_input('Task (col=1,ori=2)?: '))]

		keyboard_layout = raw_input('Color task location (l/r)?:')


	scanner = 'n'#raw_input('Are you in the scanner (y/n)?: ')
	track_eyes = raw_input('Are you recording gaze (y/n)?: ')
	if track_eyes == 'y':
		tracker_on = True
	elif track_eyes == 'n':
		tracker_on = False

	# appnope.nope()
	if training == 'y':
		ts = TrainerSession( initials, run_nr, scanner, tracker_on, task )
	else:
		ts = ExpectationSession( initials, run_nr, scanner, tracker_on, task, keyboard_layout )
	ts.run()
	if training == 'n':
		plot_staircases(initials, run_nr)
   
if __name__ == '__main__':
   main()
      
