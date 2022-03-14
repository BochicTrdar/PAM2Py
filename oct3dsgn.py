from numpy import *
from scipy import signal

def oct3dsgn(Fc=None,
             Fs=None,
             N =None):
# OCT3DSGN  Design of a one-third-octave filter.
#    [B,A] = OCT3DSGN(Fc,Fs,N) designs a digital 1/3-octave filter with 
#    center frequency Fc for sampling frequency Fs. 
#    The filter is designed according to the Order-N specification 
#    of the ANSI S1.1-1986 standard. Default value for N is 3. 
#    Warning: for meaningful design results, center frequency used
#    should preferably be in range Fs/200 < Fc < Fs/5.
#
# Abbreviated from the octave toolbox by:
# Author: Christophe Couvreur, Faculte Polytechnique de Mons (Belgium)
#         couvreur@thor.fpms.ac.be
# Last modification: Aug. 25, 1997, 2:00pm.
# Python version: Orlando Camargo Rodriguez
# Faro, Seg 28 Fev 2022 12:16:43 WET 

# References: 
#    [1] ANSI S1.1-1986 (ASA 65-1986): Specifications for
#        Octave-Band and Fractional-Octave-Band Analog and
#        Digital Filters, 1993.

    A = []
    B = []
    pi = 3.14159265358979
    factor = 10**( 1.0/20.0 )
    f1 = Fc/factor
    f2 = Fc*factor 
    Qr = Fc/( f2 - f1 )
    Qd = ( pi/(2.0*N) )/( sin( pi/(2.0*N) ) )*Qr
    alpha = ( 1.0 + sqrt( 1.0 + 4.0*Qd**2 ) )/( 2.0*Qd ) 
    W1 = Fc/( 0.5*Fs*alpha ) 
    W2 = Fc/( 0.5*Fs )*alpha
    #B,A = signal.butter(N,[W1,W2],btype='band')
    B,A = signal.cheby1(N,[W1,W2],btype='band',rp=0.15) # IEC 61260
    return B,A

