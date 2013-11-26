#! /usr/bin/env python2.7
from master import Task

def user_sum(L):
	return sum(L)

def completed(task):
	out = task.get_solutions()
	sol = [int(x) for x in out]
	print sum(sol)

if __name__ == '__main__':
	num_tasks = 1
	task = Task(num_tasks, completed)
	L = range(428)
	for i in range(num_tasks):
		task.peon_task("user_sum", i, [L])

