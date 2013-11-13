#! /usr/bin/env python2.7
from master import Task

def user_sum(L):
	return sum(L)

def completed(task):
	out = task.get_solutions()
	sol = [int(x) for x in out]
	print sum(sol)

if __name__ == '__main__':
	task = Task(completed)

	for i in range(2):
		task.peon_task("user_sum", i)
