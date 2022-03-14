# Reading data from a edf h5 file
# Faro, Ter 09 Fev 2021 16:23:24 WET  
# Written by Orlando Camargo Rodriguez
# python3 test_readedf.py

import os

# Import the function:
from read_edf import *

# Define the input filename:
filename = 'Sine_10s_48kHz_+-0.5.h5'

# Read the file, get the data: 
if os.path.exists(filename):
   data = read_edf(filename)
   print( data ) # Print the data
else: 
   print(filename + ' not found, generate the EDF file first...' )
