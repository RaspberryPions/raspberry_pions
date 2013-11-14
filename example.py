#! /usr/bin/env python2.7
from master import Task

def user_sum(L):
	return sum(L)

def completed(task):
	out = task.get_solutions()
	sol = [int(x) for x in out]
	print sum(sol)

if __name__ == '__main__':
	num_tasks = 2
	task = Task(num_tasks, completed)

	for i in range(num_tasks):
		task.peon_task("user_sum", i, [1, 2, 3, 4])
