import numpy as np

bins = [1, 3, 5]
NUM_DATA = 148

cosvalues = []
sinvalues = []
coeffvalues = []

for x in range(0,len(bins)):
    binnum = bins[x]
    w = 2.0*np.pi*binnum/NUM_DATA
    cosvalues.append(np.cos(w))
    sinvalues.append(np.sin(w))
    coeffvalues.append(2*np.cos(w))

print cosvalues
print sinvalues
print coeffvalues
