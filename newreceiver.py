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


def receiveDataAndFFT(NUM_DATA, data, magnitudedata):
	ser.flushInput()
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


NUM_DATA = 128;

data1 = []
data2 = []
magdata = []
receiveDataAndFFT(NUM_DATA, data1, magdata);
receiveDataAndFFT(NUM_DATA, data2, magdata);
error = np.sum((data1 - data2) ** 2)
print error

data2 = []
magdata = []
receiveDataAndFFT(NUM_DATA, data2, magdata);
error = np.sum((data1 - data2) ** 2)
print error

