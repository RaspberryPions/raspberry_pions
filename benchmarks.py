#! /usr/bin/env python2.7
from master import Task
import itertools

def create_matrix(n, filler):
	c = []
	for i in range(n):
	   c.append([])
	   for j in range(n): 
	     c[i].append(i + filler) 

	# print(c)
	return c  

# def multiply_square_matrices(m1, m2):
# 	l = len(m1)
# 	c = []
# 	for i in range(l):
# 		c.append([])
# 		for j in range(l): 
# 			c[i].append(0) 
# 			for k in range(l):
# 				c[i][j] = c[i][j] + m1[i][k] * m2[k][j]

# 	print(c)
# 	return c

def multiply_square_matrices(m1, m2):
	c = []
	for i in range(len(m1)):
		c.append([])
		for j in range(len(m2)): 
			c[i].append(0) 
			for k in range(len(m2)):
				c[i][j] = c[i][j] + m1[i][k] * m2[k][j]

	print(c)
	return c


def completed(task):
	out = task.get_solutions()
	solution_parts = [eval(x) for x in out] 
	sol = list(itertools.chain(*solution_parts))
	print(sol)


if __name__ == "__main__":
	m_size = 4
	m1 = create_matrix(m_size, 1)
	m2 = create_matrix(m_size, 2)

	num_tasks = 2
	task = Task(num_tasks, completed)

	slice_size = m_size/num_tasks

	slice_ind = 0
	for i in range(num_tasks):
		m1_slice = m1[slice_ind: slice_ind + slice_size]
		task.peon_task("multiply_square_matrices", i, [m1_slice, m2])
		slice_ind += slice_size
