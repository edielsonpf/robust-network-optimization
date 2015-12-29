
from random import random
from math import pow, sqrt

DARTS=1000000
hits = 0
throws = 0
for i in range (1, DARTS):
    throws += 1
    x = random()
    y = random()
    dist = sqrt(pow(x, 2) + pow(y, 2))
    if dist <= 1.0:
        hits = hits + 1.0

# hits / throws = 1/4 Pi
pi = 4 * (hits / throws)

print "hits = %s" %(hits)
print "throws = %s" %(throws)
print "pi = %s" %(pi)