# Performs pressure waveform analysis for PAMGuide.
# Adapted from PG_Waveform.m, by Nathan D. Merchant
# Faro, Seg 01 Fev 2021 21:33:24 WET 
# Written by Orlando Camargo Rodriguez
#==========================================================================
# Don't like it? Don't use it...
#==========================================================================

from numpy import *
from scipy import *
import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

def PG_Waveform(xbit   =None,
                Fs     =None,
                S      =None,
                ctype =None):
#======================================================================
    A = xbit
    dt = 1.0/Fs
    if ( ctype != 'None' ):
        A = xbit/( 10**(S/20.0) ) # apply sensitivity correction factor
                                  # EQUATION 21 
    xbit = []
    xl = A.size                 # length of input
    tmax = (xl - 1 )*dt
    t = linspace(0,tmax,xl)    # time vector
    f = ones(2)
#======================================================================
    return A,f,t
