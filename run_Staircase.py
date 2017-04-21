import sys, datetime
# from Tkinter import *

from IPython import embed

sys.path.append( 'exp_tools' )

from ExpectationSession import *

# useTracker = True

def main():
   initials = raw_input('Subject initials: ')
   # run_nr = int(raw_input('Run number: '))
   # task = (1,2)#int(raw_input('Task (col=1,ori=2)?: '))
   scanner = 'n'#raw_input('Are you in the scanner (y/n)?: ')
   track_eyes = 'n'#raw_input('Are you recording gaze (y/n)?: ')
   if track_eyes == 'y':
      tracker_on = True
   elif track_eyes == 'n':
      tracker_on = False

   # appnope.nope()

   ts = ExpectationSession( initials, 0, scanner, tracker_on, task )
   ts.run()

   # plot_staircases(initials, run_nr)
   
if __name__ == '__main__':
   main()
      
