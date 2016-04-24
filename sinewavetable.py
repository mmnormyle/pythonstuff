import numpy as np
import matplotlib.pyplot as plt

lookuptable = []

N = float(256)
max_num = float(64)
A = max_num/2
frequencies = [1, 3, 5]

num_f = float(len(frequencies))

for n in range(0, int(N)):
	value = 0
	for y in range(0, len(frequencies)):
		value = float(value) + (A/num_f)*np.sin(2*np.pi*float(frequencies[y])*float(n)/N)	
	value = value + A	
	lookuptable.append(int(np.round(value)))

for x in range (0, len(lookuptable)):
	print(str(lookuptable[x]) + ','),
	if((x+1)%8==0):
		print

plt.plot(lookuptable)
plt.show()
