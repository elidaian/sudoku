from time import time
from sudoku.generator import generate

__author__ = "Eli Daian <elidaian@gmail.com>"

NUM_ITERATIONS = 20

a = time()
for i in xrange(NUM_ITERATIONS):
    board = generate(3, 4)
b = time()

print 'Took %.2f seconds' % ((b - a) / NUM_ITERATIONS)

# Regular: Took 0.42 seconds
# Dodeka: Took 2.06 seconds
