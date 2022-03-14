# Computes calibrated acoustic spectra from (lossless) digital audio files.
# Adapted from PG_Func.m, by Nathan D. Merchant
# Faro, Qua Out 20 20:30:29 WEST 2021
# Written by Orlando Camargo Rodriguez
#==========================================================================
# Don't like it? Don't use it...
#==========================================================================

#
#WAV format             Min       Max        NumPy dtype
#32-bit floating-point -1.0      +1.0        float32
#32-bit integer PCM  -2147483648 +2147483647 int32
#24-bit integer PCM  -2147483648 +2147483392 int32
#16-bit integer PCM  -32768      +32767      int16
# 8-bit integer PCM   0           255        uint8

from numpy import *
from scipy import *
import soundfile as sf
import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
from PG_Waveform import *
from PG_DFT      import *
from PG_TOL      import *
from PG_Viewer   import *

def PG_Func(ifile    =None,
            atype    =None,
            plottype =None,
            envi     =None,
            ctype    =None,
            Si       =None,
            Mh       =None,
            G        =None,
            vADC     =None,
            r        =None,
            wlength  =None,
            winname  =None,
            lcut     =None,
            hcut     =None,
            welch    =None,
            linlog   =None):
#======================================================================
    A = []
    f = []
    t = []
#======================================================================
    S = 0.0

    thesignal, Fs = sf.read(ifile,dtype=float64) # Let's hope we always get -1 < thedata < 1

    samples_channels = squeeze( thesignal.shape )
    if samples_channels.size == 1:
       samples  = samples_channels
       channels = 1
       xbit     = thesignal; thesignal = []
    else:
       samples  = samples_channels[0]
       channels = samples_channels[1]
       xbit     = thesignal[0,:]; thesignal = []

    xbit = float32( xbit ) # Single precision
    nyquist = int( Fs/2 )
    N = int( Fs*wlength )

    print( 'Analysis type: ' + str(atype))
    print( 'Plot type: '  + str(plottype))
    if ( envi == 'Air' ): 
       Mh = Mh - 120 # convert to dB re 1 V/uPa
       print('Measurement: In-air.')
    else:
       print('Measurement: Underwater.')
    if ( ctype == 'EE' ):
       S = Si
       print('End-to-end system sensitivity = ' + str(Si) + ' dB')
    elif ( ctype == 'RC' ):
       S = Si + Mh
       print('System sensitivity of recorder (excluding transducer) = ' + str(Si) + ' dB')
       if ( envi == 'Air' ):
          print('Microphone sensitivity, Mh = ' + str(Mh) + ' dB re 1 V/Pa')
       else:
            print('Hydrophone sensitivity, Mh = ' + str(Mh) + ' dB re 1 V/uPa')
    elif ( ctype == 'TS' ):
       S = Mh + G + 20*log10( 1.0/vADC )
       if envi == 'Air':
          print('Microphone sensitivity, Mh = ' + str(Mh) + ' dB re 1 V/Pa')
       else:
            print('Hydrophone sensitivity, Mh = ' + str(Mh) + ' dB re 1 V/uPa')
    else:
       print('Uncalibrated analysis. Output in relative units.')
    print('System sensitivity correction factor S = ' + str(S) + ' dB' )    
    print('Preamplifier gain, G = ' + str(G) + ' dB')
    print('ADC peak voltage, vADC = ' + str(vADC) + ' V')
    print('Sampling frequency, Fs = ' + str(Fs) + ' Hz')
    print('Time segment length: ' + str(N) + ' samples = ' + str(N/Fs) + ' s')
    print('Window function: ' + winname)
    print('Time segment overlap: ' + str(100*r) + ' %')
    if ( welch > 0.0 ):
       message = 'Welch factor = ' + str(welch) + 'x' 
       print( message )
       message = 'New time resolution = ' + str(welch) + ' (Welch factor) x ' + str(N/Fs) + ' s (time segment length) x ' + str(r*100) + ' %% (overlap) = ' + str(welch*r*N/Fs),' s'
       print( message )
    else:
       message = 'Welch factor = 0'
       print( message )
#======================================================================
    if atype == 'Waveform':    # pressure waveform
       A,f,t = PG_Waveform(xbit,Fs,S,ctype)
    elif atype == 'PSD':       # power spectral density
       A,f,t = PG_DFT(xbit,Fs,S,N,r,winname,envi,lcut,hcut,atype)
    elif atype == 'PowerSpec': # power spectrum (for tonal amplitudes)
       A,f,t = PG_DFT(xbit,Fs,S,N,r,winname,envi,lcut,hcut,atype)
    elif atype == 'TOLf':      # standard TOL implementation using filters
       A,CI,f,t = PG_TOL(xbit,S,Fs,N,envi,lcut,hcut,plottype,ctype,ifile)
    elif atype == 'TOL':       # fast TOL implementation using DFT
       A,f,t = PG_DFT(xbit,Fs,S,N,r,winname,envi,lcut,hcut,atype)
    elif atype == 'Broadband': # broadband level
       A,f,t = PG_DFT(xbit,Fs,S,N,r,winname,envi,lcut,hcut,atype)
    else:                      # catch typos
       print('Analysis type not recognised. PAMGuide aborted.')
#======================================================================
## REDUCE TIME RESOLUTION BY WELCH METHOD IF SELECTED
# Welch method (EQUATION 20)
    if ( welch > 0 ):
       rA = t.size # number of rows    in array
       cA = f.size # number of columns in array
       lout = int( ceil(rA/welch) ) # length  of output array
       if ( ( lout == 2 ) and ( lout != 1 )  ):
          print('Welch factor too large:') 
          print('reduction in time resolution longer than 1/2 the file, taking Welch = 0...')
       else:
          AWelch = zeros((lout,cA)) # initialize output array
          tWelch = zeros(lout)
          tint = t[1]- t[0]         # time window interval
          for i in range(lout):
              stt = t[0] + i*tint*welch               # start time
              ett = stt + welch*tint                  # end   time
              tWelch[i] = stt                         # stamp with start time
              indexes = ( t >= stt ).nonzero()[0]     # find start index
              sti = indexes[0]+1
              indexes = ( t <  ett ).nonzero()[0]     # find end   index
              eti = indexes[-1]+1
              if ( eti > sti ):
                 nowA = 10**( A[sti:eti+1,:]/10.0 )
                 AWelch[i,:] = 10*log10( mean(nowA,axis=0) ) # write mean to new array
              elif ( eti == sti ):
                 nowA = 10**( A[sti,:]/10.0 )
                 AWelch[i,:] = 10*log10(nowA)         # if only one window in range
              else:
                 AWelch[i,:] = NaN
          first_column = 0*AWelch[:,0]
          indexes = ( first_column == 0.0 ).nonzero()[0]
          A = AWelch[indexes,:] # reassign output as Welch array
          t = tWelch[indexes  ]
          AWelch = []
          tWelch = []
#======================================================================
# Scale relative analyses to 0 dB
    if ( ctype == 'None' ):
       if ( atype == 'Waveform' ):
          A = A/amax( abs( A ) ) # if uncalibrated, scale relative pressure to +/- 1
       else:
          A = A - amax( A )
#======================================================================
## ENCODE TIME-DOMAIN ARRAY WITH ANALYSIS METADATA

    if ( atype == 'PSD' ): 
       aid = 1
    elif ( atype == 'PowerSpec' ):
       aid = 2
    elif ( ( atype == 'TOL' ) or ( atype == 'TOLf') ): 
       aid = 3
    elif ( atype == 'Broadband' ): 
       aid = 4
    elif ( atype == 'Waveform' ):
       aid = 5
    else:
       aid = 0

    if ( ctype != 'None' ): 
       aid = aid + 10
    else: 
       aid = aid + 20

    if ( envi == 'Air'): 
       aid = aid + 100
    else: 
       aid = aid + 200
    
    aid = aid + 2000
#======================================================================
## PLOT DATA, INCLUDING STATS IF SELECTED
    PG_Viewer(A,f,t,aid,plottype,ifile,linlog)
#======================================================================
    return
