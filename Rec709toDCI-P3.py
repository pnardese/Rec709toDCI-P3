"""
Rec709toDCI-P3.py version 0.1
Rec.709 to DCI P3 LUT generation, as per RP 177-1993
http://car.france3.mars.free.fr/HD/INA-%2026%20jan%2006/SMPTE%20normes%20et%20confs/rp177.pdf

Davinci Resolve .dat LUT format

"""

import numpy as np
from numpy.linalg import inv 

"""
DCI P3 types
D65 = 0 no CAT
D60 = 1
Theater = 2
"""
DCI_P3_type = 2

# define LUT_size
LUT_size = 33

#DCI P3 D65 no CAT http://www.haraldbrendel.com/colorspacecalculator.html
if DCI_P3_type == 0: 
	TRA = np.array([[0.822462, 0.177538, 0.000000],
 					[0.033194, 0.966806, 0.000000],
 					[0.017083, 0.072397, 0.910520]])

#DCI P3 D60 http://www.haraldbrendel.com/colorspacecalculator.html
elif DCI_P3_type == 1: 
	TRA = np.array([[0.806090, 0.190312, 0.003599],
					[0.032717, 0.965705, 0.001578],
 					[0.016834, 0.071717, 0.911450]])

#DCI P3 Theater http://www.haraldbrendel.com/colorspacecalculator.html
elif DCI_P3_type == 2: 
 	TRA = np.array([[0.868580, 0.128919, 0.002501],
 					[0.034540, 0.961811, 0.003648],
 					[0.016771, 0.071040, 0.912189]])					 

delta = 1.0 / (LUT_size - 1)

print 'LUT_3D_SIZE', LUT_size, '\n'

for r in range(LUT_size):
	for g in range(LUT_size):
		for b in range(LUT_size):

			"""
			Linearize 709
			
			""" 

			Vr = r * delta
			Vg = g * delta
			Vb = b * delta

			if Vr < 0.081:
				rLinear = Vr / 4.5
			else:
				rLinear = pow(((Vr + 0.099) / 1.099), 1.0 / 0.45) 
			
			if Vg < 0.081:
				gLinear = Vg / 4.5
			else:
				gLinear = pow(((Vg + 0.099) / 1.099), 1.0 / 0.45) 
			
			if Vb < 0.081:
				bLinear = Vb / 4.5
			else:
				bLinear = pow(((Vb + 0.099) / 1.099), 1.0 / 0.45) 
			
			"""
			Transform linear 709 to DCI-P3

			"""

			RGBlinear = np.array([rLinear, gLinear, bLinear])
			
			RGB_DCI_P3 = np.dot(TRA, RGBlinear)

			
			"""
			DCI-P3 gamma 2.6 V = V **(1/2.6)

			"""

			if RGB_DCI_P3[0] > 0:
				Vr_gamma_DCI_P3 = pow(RGB_DCI_P3[0], 1.0 / 2.6)
			else:
				Vr_gamma_DCI_P3 = 0
			if RGB_DCI_P3[1] > 0:
				Vg_gamma_DCI_P3 = pow(RGB_DCI_P3[1], 1.0 / 2.6)
			else:
				Vg_gamma_DCI_P3 = 0
			if RGB_DCI_P3[2] > 0:
				Vb_gamma_DCI_P3 = pow(RGB_DCI_P3[2], 1.0 / 2.6)
			else:
				Vb_gamma_DCI_P3 = 0

			print Vr_gamma_DCI_P3, Vg_gamma_DCI_P3, Vb_gamma_DCI_P3









