import struct
import serial
from fractions import Fraction
import numpy as np
import matplotlib.pyplot as plt

N = 64

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
	port='/dev/ttyACM0',
	baudrate=9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS
)

NUM_DATA = 64

#ser.open()
ser.isOpen()

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

q0 = 0
q1 = 0
q2 = 0
maxval = 0;

f_coeff = []
f_cos = []
f_sin = []
bins = [1]

for x in range(0,len(bins)):
        print "For bin: " + str(bins[x])
        K = bins[x];
        Wo = 2.0*np.pi/N*K

        cos_val = np.cos(Wo);
        coeff = 2*np.cos(Wo);
        sin_val = np.sin(Wo);

        for x in range(0,N):
            if(q1>maxval):
                maxval = q1
            q0 = coeff*q1 - q2 + data[x];
            q2 = q1;
            q1 = q0;

        real = q1*cos_val - q2;
        imag = q1*sin_val;

        maxmult = 2147483647.0/maxval;

        coeff_fixed =  Fraction(coeff).limit_denominator(int(maxmult/2))
        cos_fixed =  Fraction(cos_val).limit_denominator(int(maxmult))
        sin_fixed = Fraction(sin_val).limit_denominator(2000)

        z0 = np.int32(0)
        z1 = np.int32(0)
        z2 = np.int32(0)
        maxval = 0;

        for x in range(0,N):
            if(coeff_fixed.numerator*z1>maxval):
                maxval = coeff_fixed.numerator*z1
            z0 = (coeff_fixed.numerator*z1)/coeff_fixed.denominator - z2 + data[x];
            z2 = z1;
            z1 = z0;
               
        fixed_real = (z1*cos_fixed.numerator)/cos_fixed.denominator - z2;
        fixed_imag = (z1*sin_fixed.numerator)/sin_fixed.denominator;

        print "real: " + str(real)
        print "imag: " + str(imag)
        print "fixed real: " + str(fixed_real)
        print "fixed_imag: " + str(fixed_imag)
        print "off real: " + str((fixed_real-real)/real)
        print "off imag: " + str((fixed_imag-imag)/imag)
        print "Coeff values: "
        print coeff_fixed
        print "Cos values: "
        print cos_fixed
        print "Sin values: "
        print sin_fixed
        print
        print
        print
        f_coeff.append(coeff_fixed)
        f_cos.append(cos_fixed)
        f_sin.append(sin_fixed)

print "const int32_t COS_NUM[] = {",
for x in range(0, len(bins)):
    print(f_cos[x].numerator), 
    if(x!=(len(bins)-1)):
        print(","),
print "};"
print "const int32_t COS_DEN[] = {",
for x in range(0, len(bins)):
    print(f_cos[x].denominator),    
    if(x!=(len(bins)-1)):
        print(","),
print "};"


print "const int32_t SIN_NUM[] = {",
for x in range(0, len(bins)):
    print(f_sin[x].numerator),    
    if(x!=(len(bins)-1)):
        print(","),
print "};"
print "const int32_t SIN_DEN[] = {",
for x in range(0, len(bins)):
    print(f_sin[x].denominator),
    if(x!=(len(bins)-1)):
        print(","),
print "};"


print "const int32_t COEFF_NUM[] = {",
for x in range(0, len(bins)):
    print(f_coeff[x].numerator), 
    if(x!=(len(bins)-1)):
        print(","),
print "};"
print "const int32_t COEFF_DEN[] = {",
for x in range(0, len(bins)):
    print(f_coeff[x].denominator),
    if(x!=(len(bins)-1)):
        print(","),
print "};"

