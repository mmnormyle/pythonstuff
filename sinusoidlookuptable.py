import numpy as np

cos_lookuptable = []
sin_lookuptable = []

data_size = 128
scale = 8

for n in range(0, data_size):
	cos_lookuptable.append(int(
		np.cos(2*np.pi*float(n)/float(data_size)) * pow(2,scale)))
	sin_lookuptable.append(int(
		np.sin(2*np.pi*float(n)/float(data_size)) * pow(2,scale)))

	
#for x in range (0, len(cos_lookuptable)):
#	print(str(float(cos_lookuptable[x])/float(pow(2,scale)) - np.cos(2*np.pi*float(x)/float(data_size)) ) + ','),
#	if((x+1)%8==0):
#		print
print "cos: "
for x in range (0, len(cos_lookuptable)):
	print(str(cos_lookuptable[x]) + ','),
	if((x+1)%8==0):
		print

print
print "sin: "
for x in range (0, len(sin_lookuptable)):
	print(str(sin_lookuptable[x]) + ','),
	if((x+1)%8==0):
		print
