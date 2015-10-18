import numpy as np

#
# 0. DAC Stage
#
Fu = 0.0 #update frequency of dac
DacBits = 0.0 #number of bits in DAC
N = 64.0 #number of points in sine wave lookup table
MaxValueLookup = 0.0 #max value in sine wave lookup table
Vref = 0.0 #measured value of Vref for DAC

Fo = Fu/N #base frequency of DAC sine wave
Ao = MaxValueLookup/(pow(2.0,DacBits))*Vref/2.0 #amplitude of DAC sine wave
Po = 0.0 #phase of DAC sine wave

#
# 1. VCCS Stage
#

PhaseVCCS = 0.0 #phase shift of VCCS
GainVCCS = 0.0 #gain of VCCS

Ac = Ao*GainVCCS #amplitude of current wave
Pc = PhaseVCCS + Po #phase of current wave

#
# Load Stage
#

Rl = 0.0 #resistance of load
Cl = 0.0 #capacitance of load
GainLoad = 0.0 #gain of load (function of Rl and Cl)
PhaseLoad = 0.0 #phase shift of load (function Rl and Cl)

Al = GainLoad*Ac
Pl = PhaseLoad + Pc

#
# Signal Conditoning Stage
#

GainSC = 0.0 #gain of signal conditioner
PhaseSC = 0.0 #phase shift of signal conditioner

An = GainSC*Al
Pn = PhaseSC + Pl

#
# ADC Sampling
#

Vrplus = 3.3 #positive reference voltage for ADC
Vrminus = 0.0 #negative reference voltage for ADC

GainADC = 16384.0 * (An - Vrminus)/(Vrplus - Vrminus) #gain of ADC (convesion to number)
PhaseADC = 0.0 #measured phase shift of ADC

Af = GainADC*Al
Pf = PhaseADC + Pn


