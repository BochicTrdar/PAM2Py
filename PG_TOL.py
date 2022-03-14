# Performs 1/3-octave analysis for PAMGuide.m using the standard filter bank method.
# Written by Orlando Camargo Rodriguez
# Adapted from PG_TOL.m, by Nathan D. Merchant
# Faro, Seg 28 Fev 2022 12:48:25 WET 
#==========================================================================
# Don't like it? Don't use it...
#==========================================================================

from numpy    import *
from scipy    import *
from scipy    import signal
from buffer   import *
from oct3dsgn import *
from matplotlib.pyplot import *

def PG_TOL(xbit    =None,
           S       =None,
           Fs      =None,
           N       =None,
           envi    =None,
           lcut    =None,
           hcut    =None,
           plottype=None,
           ctype   =None,
           ifile   =None):
#======================================================================
    A  = []
    CI = []
    fc = []
#======================================================================
    if envi == 'Air':
       pref = 20.0
    else:
       pref = 1.0
    pxp = pref*pref
#======================================================================
    if ctype == 'None':
       calib = 0
    else:
       calib = 1
#======================================================================
    if ( N < Fs ):
       N = Fs # set N >= 1 s for TOL analysis

    T = 1.0*N/Fs # convert N in samples into T in seconds

    if ( lcut < 25 ):
       lcut = 25 # limit low cut-off frequency to 25 Hz

    xold    = []
    naveold = []

    fkey = 1000                           # ANSI standard key frequency
    #oRd  = 3                             # third octave filter order - Butterworth
    oRd  = 4                              # third octave filter order - Chebyshev
    ndec = 24                             # length of decimating FIR filter
    za   = 1.6                            # multiplier on sigma for a 90% confidence interval
    nta = int( floor( log(  Fs/3.0/fkey)/log(2.0)*3) ) + 1 # number of third octaves above key frequency
    ntb = int( floor(-log(1.0*lcut/fkey)/log(2.0)*3) ) + 1 # number of third octaves below key frequency
    indexes = arange(nta,-ntb-1,-1)
    fc = fkey*10**( indexes/10.0 ) # center frequencies of the third octaves to analyse, high to low
    nc = fc.size
# design a filter for the top three third octaves
    B = zeros( (3,2*oRd+1) )
    A = zeros( (3,2*oRd+1) )
    nave = int( round(T*Fs) )                 # number of samples to average in the top octave
    a = zeros((int(floor(xbit.size/nave)),nc)) # make space for the results
    CI = zeros(nc)
#======================================================================
    for k in range(nc):                 # loop for each third octave
        ton = remainder(k,3)+1          # find out which filter to use
        B[ton-1,:],A[ton-1,:] = oct3dsgn(fc[k],Fs,oRd) # make filter
        y = signal.lfilter(B[ton-1,:],A[ton-1,:],xbit)  # apply the filter
        Y = buffer(y,nave,0,'nodelay')    # break up the filter output in T-length blocks
        Ycols = Y[0,:].size
        if ( k == 0 ):
           Ycols1 = Ycols
        elif ( Ycols != Ycols1 ):      # if decimated x yields different number of T-length blocks
           B[ton-1,:],A[ton-1,:] = oct3dsgn(fc[k],Fs*2,oRd) # keep previous fs
           y = signal.lfilter(B[ton-1,:],A[ton-1,:],xold)    # apply the filter
           Y = buffer(y,naveold,0,'nodelay')            # break up the filter output in T-length blocks
        a[:,k] = 10*log10( mean(Y**2,axis=0)/pxp) - S   # record the power in each block in dB
        CI[k] = 0.5/sqrt(0.23*fc[k]*nave/Fs)  # 1/(2sqrt(B*T)), B = (2^(1/6)-2^(-1/6))fc = 0.23fc
        if ( ( ton == 3 ) and ( Ycols == Ycols1 ) ): # after each third TOL, decimate by 2 for the next octave
           xold = xbit                     # store previous x iteration
           naveold = nave                  # store previous nave iteration
           xbit = signal.decimate(xbit,2,ndec,'fir') # do the decimation
           Fs = Fs/2                         # update the sampling rate and number of samples to average
           nave = int( round(Fs*T) )
#======================================================================
    a = a[:,::-1]  # reorder the results from low to high
    fc = fc[::-1]  # and eliminate any unanalysed third octaves.
    M = zeros((nc,2))
    M[:,0] = maximum(1.0-za*CI,0)
    M[:,1] = 1.0 + za*CI
    CI = []
    CI = 20*log10( M )
    CI = CI[::-1,:]
#======================================================================
# Scale relative analyses to 0 dB
    if ( ctype == 'None' ):
       a = a - amax(a)
#======================================================================
## Plot data

    ttot = a[:,0].size*T - T # total time  in seconds
    t = arange(0,ttot+T,T)   # time vector in seconds
    A = []
    A = a
    a = []
    if ( ( plottype == 'Time' ) or ( plottype == 'Both' ) ):
       #Initialize figure window
       figure()
       faux = fc*10**(-0.05)
       yscale('log')
       pcolormesh(t,faux,A.transpose(),cmap='viridis',shading='auto')
       cb = colorbar()
       xlim(t[0],t[-1])
       ylim(faux[0],faux[-1])
       xlabel('Time [ s ]')
       ylabel('Frequency [ Hz ]')
       if ( calib == 1 ):
          cb.set_label(r'1/3-octave SPL [ dB re ' + str(pref) + ' $\mu$Pa ]',fontsize=14)
       else:
          cb.set_label('Relative 1/3-octave SPL [ dB ]',fontsize=14)
       title('1/3 Octave Analysis of ' + ifile + '. Window length = ' + str(T) + ' s = ' + str(N) + ' samples.' )
       print('Close the figure to proceed with calculations...')
#       show()
#======================================================================
    return A,CI,fc,t
