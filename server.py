# TODO: while we are listening, we have to check whether pions are okay (not dead, not frozen, etc.)
# if dead, we can't do much
# if frozen, can we reboot them from master?
 
# we have to make sure it is a singleton

from socket import *

try:
    import RPi.GPIO as GPIO # general purpose input-output for the RP
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")


class Task(object):

    def __init__(self):
        self.answers = []
        self.error = None
        self.required_pions = 5 # this is supposed to change based on the job delegation. ie: what if we need just 3 pions? 
        
        self.HOST = 'localhost'
        self.PORT = 5001
        
        # we can take listen out of init step and let user decide when they want it. 
        # i just think the earlier it gets run, the better, because then we decrease the chance of missing a job returning from a peon 
        self.listen() 
                    
        
    def peon_task(self, func, id, work_unit, extra_args=[]):
        # send the function to the peon with the self.port number
        pass

    def listen(self):

        s = socket(AF_INET, SOCK_STREAM)
        s.bind((self.HOST, self.PORT))
        working_pions = self.required_pions   

        s.listen(working_pions) # number of pions that can wait in queue

        # this loop has to be heavily modified with respect to actual server receiving connection rules
        while working_pions != 0:
            conn = s.accept()        
            ans, id = # get data from peon
            
            # validate the data:
            # if pion reported an error, try job with another free pion, if that fails again, we write error result in self.error.
            # we could also overwrite answers, but i don't think it's good
            
            # if data is valid
            answers[id] = ans
            working_pions -=1
            
        # if we are out of the loop, all jobs are done, we will just have to signal that to the user.
