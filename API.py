#!/usr/bin/env python        

# Sample API usage

from raspberry_pions import Task

work_segments = [] # an initial list of work defined by the user
task = Task() # create an instance of the Task that sets up the server. 

for i in range (0, len(work_segments)):
    task.peon_task(func, i, work_segments[i])

# wait for signal that job is done, have to come up with that
# after the signal 
return task.answers
    

