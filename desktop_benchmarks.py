#! /usr/bin/env python2.7

import time

def create_matrix(n, filler):
	c = []
	for i in range(n):
	   c.append([])
	   for j in range(n): 
	     c[i].append(i + filler) 

	# print(c)
	return c  

def multiply_square_matrices(m1, m2):
	l = len(m1)
	c = []
	for i in range(l):
		c.append([])
		for j in range(l): 
			c[i].append(0) 
			for k in range(l):
				c[i][j] = c[i][j] + m1[i][k] * m2[k][j]

	print(c)
	return c


def completed(task):
	out = task.get_solutions()
	sol = [eval(x) for x in out] 
	print(sol)


if __name__ == "__main__":
	m1 = create_matrix(3, 1)
	m2 = create_matrix(3, 2)

	t1 = time.clock()
	m3 = multiply_square_matrices(m1, m2)
	t2 = time.clock()
	runtime = t2 - t1
	print(runtime)
