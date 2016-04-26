#This script calculates Goertzel coefficients for both floating point and fixed point.
#Floating point is easy.
#Fixed point requires balancing an accurate fraction with overflow.

import struct
import serial
from fractions import Fraction
import numpy as np
import matplotlib.pyplot as plt
import sys

#number of data point in sample
N = 148
#max value read from MSP432 ADC
ADC_AMPLITUDE = 16384
#desired goertzel bins to calculate
bins = [1, 3, 5]
#maximum shift amount ^ 2
SHIFT_AMOUNT = 256


data = []

#If there's a command line argument, grab real data through UART from the MCU
if(len(sys.argv)>1):
        # configure the serial connections (the parameters differs on the device you are connecting to)
        ser = serial.Serial(
            port='/dev/ttyACM0',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )

        #ser.open()
        ser.isOpen()

        ser.flushInput()
        data = []
        magnitudedata = []
        while len(data)<N:
                if(ser.inWaiting>0) :
                    if(ser.read(1)=='a'):
                        while(ser.inWaiting<4):
                            pass
                        value = struct.unpack('<i', ser.read(4))[0]
                        data.append(value)
else:
    for x in range(0,N):
        data.append((ADC_AMPLITUDE/2)*np.sin(2.0*np.pi/N*x) + (ADC_AMPLITUDE/2))


fixed_coeff = []
fixed_cos = []
fixed_sin = []

float_coeff = []
float_sin = []
float_cos = []

for x in range(0,len(bins)):

        q0 = 0
        q1 = 0
        q2 = 0
        maxval = 0

        print "For bin: " + str(bins[x])
        K = bins[x];
        Wo = 2.0*np.pi/N*K

        cos_val = np.cos(Wo);
        coeff = 2*np.cos(Wo);
        sin_val = np.sin(Wo);

        float_coeff.append(coeff)
        float_sin.append(sin_val)
        float_cos.append(cos_val)

        for x in range(0,N):
            if(q1>maxval):
                maxval = q1
            q0 = coeff*q1 - q2 + data[x];
            q2 = q1;
            q1 = q0;

        print "Maximum value of z1: " + str(maxval)

        real = q1*cos_val - q2;
        imag = q1*sin_val;

        maxmult = 2147483647.0/(maxval/SHIFT_AMOUNT);

        print "The maximum numberator is: " + str(maxmult)

        coeff_fixed =  Fraction(coeff).limit_denominator(int(maxmult/2))
        cos_fixed =  Fraction(cos_val).limit_denominator(int(maxmult))
        sin_fixed = Fraction(sin_val).limit_denominator(2000)

        z0 = np.int32(0)
        z1 = np.int32(0)
        z2 = np.int32(0)
        maxval = 0;

        for x in range(0,N):
            z0 = ((coeff_fixed.numerator*(z1/SHIFT_AMOUNT))*SHIFT_AMOUNT)/coeff_fixed.denominator - z2 + data[x];
            z2 = z1;
            z1 = z0;

        fixed_real = (z1*cos_fixed.numerator)/cos_fixed.denominator - z2;
        fixed_imag = (z1*sin_fixed.numerator)/sin_fixed.denominator;

        print "off real: " + str((fixed_real-real)/real)
        print "off imag: " + str((fixed_imag-imag)/imag)
        print "Coeff values: "
        print coeff_fixed
        print "Cos values: "
        print cos_fixed
        print "Sin values: "
        print sin_fixed
        print
        fixed_coeff.append(coeff_fixed)
        fixed_cos.append(cos_fixed)
        fixed_sin.append(sin_fixed)

print "/* bin mappings are: "
for x in range(0, len(bins)):
    print " * [" + str(x) + "] ... ",
    print bins[x]
print "*/"

print "const float FLOAT_COS[] = {",
for x in range(0, len(bins)):
    print(float_cos[x]),
    if(x!=(len(bins)-1)):
        print(","),
print "};"

print "const float FLOAT_SIN[] = {",
for x in range(0, len(bins)):
    print(float_sin[x]),
    if(x!=(len(bins)-1)):
        print(","),
print "};"

print "const float FLOAT_COEFF[] = {",
for x in range(0, len(bins)):
    print(float_coeff[x]),
    if(x!=(len(bins)-1)):
        print(","),
print "};"

print "const int32_t COS_NUM[] = {",
for x in range(0, len(bins)):
    print(fixed_cos[x].numerator),
    if(x!=(len(bins)-1)):
        print(","),
print "};"
print "const int32_t COS_DEN[] = {",
for x in range(0, len(bins)):
    print(fixed_cos[x].denominator),
    if(x!=(len(bins)-1)):
        print(","),
print "};"


print "const int32_t SIN_NUM[] = {",
for x in range(0, len(bins)):
    print(fixed_sin[x].numerator),
    if(x!=(len(bins)-1)):
        print(","),
print "};"
print "const int32_t SIN_DEN[] = {",
for x in range(0, len(bins)):
    print(fixed_sin[x].denominator),
    if(x!=(len(bins)-1)):
        print(","),
print "};"

print "const int32_t COEFF_NUM[] = {",
for x in range(0, len(bins)):
    print(fixed_coeff[x].numerator),
    if(x!=(len(bins)-1)):
        print(","),
print "};"
print "const int32_t COEFF_DEN[] = {",
for x in range(0, len(bins)):
    print(fixed_coeff[x].denominator),
    if(x!=(len(bins)-1)):
        print(","),
print "};"

