# Performs DFT-based analysis (PSD,TOLf (fast 1/3-octave method),Broadband) for PAMGuide. 
# Adapted from PG_DFT.m, by Nathan D. Merchant
# Faro, Ter 15 Mar 2022 17:16:25 WET 
# Written by Orlando Camargo Rodriguez
# Includes correction C. Malinka to address bug in calculation of one-third
# octave levels which affected accuracy at low-frequencies (<~200 Hz) when 
# applying a low-frequency cut-off in the analysis
#==========================================================================
# Don't like it? Don't use it...
#==========================================================================

from numpy  import *
from buffer import *

def PG_DFT(xbit   =None,
           Fs     =None,
           S      =None,
           N      =None,
           r      =None,
           winname=None,
           envi   =None,
           lcut   =None,
           hcut   =None,
           atype  =None):
#======================================================================
    a = []
    f = []
    t = []
#======================================================================
    No2 = int( N/ 2 )
#======================================================================
    if atype == 'PSD':         # if PSD selected
       print('Computing PSD...')
    elif atype == 'PowerSpec': # if power spectrum selected
       print('Computing power spectrum...')
    elif atype == 'Broadband': # if broadband level selected
       print('Computing broadband level...')
    elif atype == 'TOL':       # if TOL selected
       print('Computing 1/3-octave levels...')
#======================================================================
    if envi == 'Air':
       pref = 20.0
    else:
       pref = 1.0
    pxp = pref*pref
#======================================================================
## COMPUTING POWER SPECTRUM 
## Divide signal into data segments (corresponds to EQUATION 5)

    xl = xbit.size
    if ( N > xl ): # check segment is shorter than file
       print('Error: The chosen segment length is longer than the file.')
    xbit = float32( xbit ) # Single precision
# Remove last row if it is padded with zeros;
# the padding should be obvious if the last value of the signal 
# has not been placed in the lower right corner of the matrix; 
# to be 100% sure we will set the last value out of range. 
    last_value = xbit[-1]
    xbit[-1] = 10.0
    xgrid = buffer(xbit,N,int(ceil(N*r)),'nodelay').transpose()
    if ( xgrid[-1,-1] != xbit[-1] ):
         aux = xgrid
         xgrid = []
         xgrid = aux[0:-1,:]
         aux = []
    else:
         xgrid[-1,-1] = last_value
    xbit = []
    M = xgrid[:,0].size # total number of data segments
## Apply window function (corresponds to EQUATION 6)
    indexes = arange(1,N+1)
    c  = cos( 2.0*pi*indexes/N )
    c2 = cos( 4.0*pi*indexes/N )
    if winname == 'None': # i.e. rectangular (Dirichlet) window
        w = ones(N)
        alpha = 1.0             # scaling factor
    elif winname == 'Hann':     # Hann window         
        w = 0.5*( 1.0 - c )
        alpha = 0.5             # scaling factor
    elif winname == 'Hamming':  # Hamming window
        w = (0.54 - 0.46*c)
        alpha = 0.54;           # scaling factor
    elif winname == 'Blackman': # Blackman window
        w = (0.42 - 0.5*c + 0.08*c2)
        alpha = 0.42            # scaling factor
    w = w/alpha
    for i in range(M):
        xgrid[i,:] = xgrid[i,:]*w # multiply segments by window function
## Compute DFT (EQUATION 7)
    X = abs( fft.fft(xgrid,axis=1) )  # calculate DFT of each data segment
    xgrid = []
# [ if a frequency-dependent correction is being applied to the signal,  
#   e.g. frequency-dependent hydrophone sensitivity, it should be applied 
#   here to each frequency bin of the DFT ]

## Compute power spectrum (EQUATION 8)

    P = (X/N)**2 # power spectrum = square of amplitude
    X = []
## Compute single-sided power spectrum (EQUATION 9)
    Pss = 2*P[:,1:int(floor(N/2))+1] # remove DC (0 Hz) component and 
                                     # frequencies above Nyquist frequency
                                     # Fs/2 (index of Fs/2 = N/2+1), divide
                                     # by noise power bandwidth.
    P = []

## Compute frequencies of DFT bins
    f = floor(Fs/2)*linspace( 1.0/No2, 1.0, No2 )
## calculate frequencies of DFT bins
    indexes = ( f >= lcut ).nonzero()[0]
    flow = indexes[0]   # low-frequency cut-off
    indexes = ( f <= hcut ).nonzero()[0]
    fhigh = indexes[-1] # high- cut-off
    f = f[flow:fhigh+1] # frequency bins in user-defined range
    nf = f.size         # number of frequency bins
## FIX to ensure Pss covers correct frequency range during TOL analysis
    Pss = Pss[:,flow:fhigh+1]
## Compute noise power bandwidth and delta(f)
    B = sum( w*w )/N # noise power bandwidth (EQUATION 12)
    delf = 1.0*Fs/N  # frequency bin width
# C. Malinka Debug 13/12/2021 - changing Pss(:,flow:fhigh) to Pss 
## Convert to dB
    if atype == 'PSD':         # if PSD selected (EQUATION 11)
       a = 10*log10( 1.0/(delf*B)*Pss/pxp ) - S
    elif atype == 'PowerSpec': # if power spectrum selected
       a = 10*log10( Pss/pxp ) - S  # EQUATION 10
    elif atype == 'Broadband': # if broadband level selected
       a = 10*log10(sum(Pss,axis=1)/pxp ) - S # EQUATION 17
    elif atype == 'TOL':       # 1/3 octave analysis (if selected)
# Generate 1/3-octave frequencies
       if ( lcut < 25 ):
          lcut = 25
       lobandf = int( floor(log10( lcut ) ) ) # lowest  power of 10 frequency for 1/3 octave band computation
       hibandf = int( ceil( log10( hcut ) ) ) # highest power of 10 frequency for 1/3 octave band computation
       nband = 10*(hibandf-lobandf) + 1 # number of 1/3-octave bands
       fc = zeros(nband)                # initialise 1/3-octave frequency vector
       fc[0] = 10**lobandf              # lowest frequency = lowest power of 10

# Calculate centre frequencies (EQUATION 13)        
    
       for i in range(1,nband):       # calculate 1/3 octave centre 
           fc[i] = fc[i-1]*10**0.1      # frequencies to (at least) precision of ANSI standard
       indexes = ( fc >= lcut ).nonzero()[0]
       i1 = indexes[0]
       indexes = ( fc <= hcut ).nonzero()[0]
       i2 = indexes[-1]
       fc = fc[i1:i2+1] # crop frequency vector to frequency range of data
       nfc = fc.size    # number of 1/3 octave bands

# Calculate boundary frequencies of each band (EQUATIONS 14-15)    
       fb = fc*10**(-0.05)               # lower bounds of 1/3 octave bands
       fb = append( fb, fc[-1]*10**0.05) # upper bound of highest band (upper
                                         # bounds of previous bands are lower
                                         # bounds of next band up in freq.)
       if ( amax(fb) > hcut ):       # if highest 1/3 octave band extends 
          nfc = nfc-1                # above highest frequency in DFT, 
          fc = fc[0:-1]              # remove highest band.

# Calculate 1/3-octave band levels (corresponds to EQUATION 16)
       P13 = zeros((M,nfc))             # initialise TOL array  
       for i in range(nfc):             #loop through centre frequencies
           indexes = ( f >= fb[i] ).nonzero()[0]
           fli = indexes[0]   # index of lower bound of band
           indexes = ( f < fb[i+1] ).nonzero()[0]
           fui = indexes[-1]  # index of upper bound of band
           for q in range(M): # loop through DFTs of data segments
               fcl = sum( Pss[q,fli:fui+1] ) # integrate over mth band frequencies
               P13[q,i] = fcl                # store TOL of each data segment
       P130 = squeeze( P13[0,:] )
       P130 = P130.astype('float')
       P130[P130 == 0] = 'nan'
       reference = 10*log10( P130/pxp )
#       reference = 10*log10( P13[0,:]/pxp )
       i2 = ( reference < -10**6 ).nonzero()[0]
#       c = not i2 # i2 = [] => c = True
       c = i2.size
#       if c == False:
       if c != 0:
          lowcut = i2[-1] + 1  # index lowest band before empty bands at low frequencies
          P13 = P13[:,lowcut:nfc+1] # remove empty low-frequency bands
          fb = fb[lowcut:nfc+2]
          fc = fc[lowcut:nfc+1]
          nfc = fc.size             # redefine nfc
       a = 10*log10( 1.0/B*P13/pxp ) - S # TOLs
       P13 = []
    Pss = []

## Compute time vector

    tint = (1.0 - r)*N/Fs            # time interval in secs between segments
    ttot = M*tint-tint               # total duration of file in seconds
    t = arange(0,ttot+tint,tint)     # time vector in seconds   

    if atype == 'TOL': 
       f = fc

#======================================================================
    return a,f,t
