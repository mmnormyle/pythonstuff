import struct
import time
import serial
import matplotlib.pyplot as plt
import numpy as np

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
	port='COM4',
	baudrate=9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS
)

NUM_DATA = 256
#ser.open()
#ser.isOpen()

ser.flushInput()
data = []
magnitudedata = []
while len(data)<NUM_DATA:
		if(ser.inWaiting>0) :
			if(ser.read(1)=='a'):
				while(ser.inWaiting<4):
					pass
				value = struct.unpack('<i', ser.read(4))[0]
				data.append(value)
				print "poop"

while len(magnitudedata)<NUM_DATA:
		if(ser.inWaiting>0) :
			if(ser.read(1)=='a'):
				while(ser.inWaiting<4):
					pass
				value = struct.unpack('<i', ser.read(4))[0]
				magnitudedata.append(value)


print 'done!'


out = np.fft.rfft(data,128)

print np.angle(out, deg=True)

powers = []
for x in range(0, len(out)):
	powers.append(abs(out[x]))


power_mean = np.mean(magnitudedata)
power_std = np.std(magnitudedata)
magXPoints = []
magYPoints = []
sigfrequencies = []
for x in range(0,NUM_DATA):
	magXPoints.append(x*915000/NUM_DATA)
	zscore = (magnitudedata[x]-power_mean)/power_std
	if(zscore>2 and x<=(NUM_DATA/2)):
		sigfrequencies.append(x)
	magYPoints.append(magnitudedata[x])

SAMPLING_FREQ = 915000

print 'It appeas that, assuming a sampling rate of 915kHz and number of points of ' + str(NUM_DATA) + ' the significant frequencies dectected are: '
for x in range(0,len(sigfrequencies)):
	frequency = sigfrequencies[x]*SAMPLING_FREQ/NUM_DATA
	print frequency

xPoints = []
yPoints = []

for x in range(0,NUM_DATA):
	xPoints.append(x)
	yPoints.append(data[x])

plt.figure(1)
plt.subplot(211)
plt.scatter(xPoints, yPoints)

#plt.subplot(212)
#plt.scatter(magXPoints, magYPoints)
plt.show()





