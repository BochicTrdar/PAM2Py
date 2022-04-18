# Plots data analysed in PAMGuide.
# Written by Orlando Camargo Rodriguez
# Adapted from PG_Viewer.m, by Nathan D. Merchant
# Faro, Seg 18 Abr 2022 20:23:04 WEST 
# To change axes values zoom in the figure.
#==========================================================================
# Don't like it? Don't use it...
#==========================================================================

import ntpath
from numpy import *
from scipy import *
from matplotlib.pyplot import * 
from scipy.io import savemat
from scipy    import stats
import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

def PG_Viewer(A       =None,
              f       =None,
              t       =None,
              aid     =None,
              plottype=None,
              ifile   =None,
              linlog  =None):
#======================================================================
    straid   = str(aid)
    tstampid = int( straid[0] )
    enviid   = int( straid[1] )
    calibid  = int( straid[2] )
    atypeid  = int( straid[3] )
    fint     = f[1] - f[0]
    cA       = f.size
    rA       = t.size
    fileName = ntpath.basename( ifile )
    fileName = fileName[0:-4]
#======================================================================
    if ( tstampid == 1 ):
         tstamp = 1
    else:
         tstamp = []

    if ( enviid == 1 ):
         pref = 20.0 
    else:
         pref = 1.0

    if ( calibid == 1 ):
         calib = 1 
    else:
         calib = 0

    if ( atypeid == 1 ):
         atype = 'PSD'
    elif ( atypeid == 2 ):
         atype = 'PowerSpec'
    elif ( atypeid == 3 ):
         atype = 'TOLf'
    elif ( atypeid == 4 ):
         atype = 'Broadband'
    elif ( atypeid == 5 ):
         atype = 'Waveform'
    elif ( atypeid == 6 ):
         atype = 'TOL'
    else: 
         atype = ' '
#======================================================================
## Time-domain plot

    if ( ( plottype == 'Time' ) or ( plottype == 'Both' ) ): # if time plot selected
      print('Plotting...')
      figure()
# Plot data
      if ( ( atype == 'PSD' ) or ( atype == 'PowerSpec' ) ):
           if ( linlog == 0 ):
              yscale('log')
           pcolormesh(t,f,A.transpose(),cmap='viridis',shading='auto')
           ylim(f[0]+0.5*fint,f[-1]-0.5*fint)
           xlim(t[0],t[-1])
           xlabel('Time [s]'        ,fontsize=14)
           ylabel('Frequency [ Hz ]',fontsize=14)
           cb = colorbar()
           if ( atype == 'PSD' ):
              title( 'Spectrogram of ' + fileName,fontsize=16)
              if ( calib == 1 ):
                 cb.set_label(r'PSD [ dB re' + str(pref) + '$\mu$Pa$^2$/Hz ]',fontsize=14)
              else:
                 cb.set_label('Relative PSD [dB]',fontsize=14)
           elif ( atype == 'PowerSpec' ):
              if ( calib == 1 ):
                 cb.set_label(r'Power Spectrum [ dB re' + str(pref) + '$\mu$Pa ]',fontsize=14)
              else:
                 cb.set_label('Relative power spectrum [ dB ]',fontsize=14)
      elif( atype == 'Broadband' ):
           title( 'Broadband SPL of ' + fileName,fontsize=16)
           plot(t,A)
           xlim(t[0],t[-1])
           xlabel('Time [s]')
           if ( calib == 1 ):
              ylabel(r'SPL [ dB re ' + str(pref) + ' $\mu$Pa ]',fontsize=14)
           else:
              ylabel('Relative SPL [ dB ]',fontsize=14)
      elif ( ( atype == 'TOLf' ) or ( atype == 'TOL' ) ):
           pcolormesh(t,f*10**(-0.05),A.transpose(),cmap='viridis',edgecolors='face',shading='auto')
           yscale('log')
           xlim(t[0],t[-1])
           ylim(f[0]*10**(-0.05),f[-1]*10**(-0.05))
           xlabel('Time [ s ]'      ,fontsize=14)
           ylabel('Frequency [ Hz ]',fontsize=14)
           cb = colorbar()
           if ( calib == 1 ):
              cb.set_label(r'1/3-octave SPL [ dB re' + str(pref) + '$\mu$Pa ]',fontsize=14)
           else:
              cb.set_label('Relative 1/3-octave SPL [ dB ]',fontsize=14)
           title( '1/3 Octave Analysis of ' + ifile,fontsize=16)
      elif ( atype == 'Waveform' ):
           plot(t,A) # plot waveform
           xlabel('Time [ s ]',fontsize=14)
           if ( calib == 1 ):
              ylabel(r'Pressure [ $\mu$Pa ]')
           else:
              ylabel('Relative pressure')
           title('Pressure waveform of ' + fileName )
           xlim(t[0],t[-1])
#======================================================================
## Statistics plot
    if ( ( ( plottype == 'Stats' ) or ( plottype == 'Both' ) ) and ( atype != 'Waveform' ) ):
       print('Computing noise level statistics...')
       M = rA

## Compute stats

#EQUATION 18
       RMSlevel = 10*log10( mean( 10**(A/10), axis=0 ) ) # calculate RMS Level
       p = zeros((cA,99))
       for i in range(99):
           p[:,i] = percentile(A,i,axis=0)
#           p[:,i] = percentile(A,i,axis=0,interpolation='linear')
#           p[:,i] = percentile(A,i,axis=0,interpolation='midpoint')
#       savemat("fp.mat",{"p":p,"f":f})
       mindB = 10*floor( amin( A/10.0 ) ) # minimum dB level rounded down to nearest 10
       maxdB = 10* ceil( amax( A/10.0 ) ) # maximum dB level rounded up   to nearest 10
#======================================================================
       if ( ( atype != 'Broadband') and ( M > 1000 ) ):

          hind = 0.1 # histogram bin width for probability densities (PD)
          dbvec = arange(mindB,maxdB+hind,hind) # dB values at which to calculate empirical PD
          d0,e =  histogram(A[:,0],dbvec)
          m = d0.size
          sA = A.shape
          sA0 = sA[0]
          sA1 = sA[1]
          d = zeros((m,sA1+1))
          # EQUATION 19
          for i in range(sA1):
              d[:,i],e =  histogram(A[:,i],dbvec)
          d[:,-1] = d[:,-2] # add dummy column for highest frequency
          d = d/(hind*M) # SPD array
          d = where( d == 0, nan, d ) # suppress plotting of empty hist bins
          if ( ( atype == 'PSD' ) or ( atype == 'PowerSpec' ) ): # axis array for SPD pcolor plot
             f2 = append(f,f[-1]) - 0.5*fint
             [X,Y] = meshgrid(f2,dbvec)
          elif ( ( atype == 'TOL' ) or ( atype == 'TOLf' ) ): 
             f2 = append(f,f[-1]*10**0.05)*10**(-0.05)
             [X,Y] = meshgrid(f2,dbvec)
#======================================================================
       if ( atype == 'Broadband' ):
            RMSlev = 10*log10(  mean( 10**(A/10) ) )
            medlev = 10*log10(median( 10**(A/10) ) )
            modelev = stats.mode( round_(10*A)/10, axis=None )[0][0]
            if ( calib == 1 ):
                 print(r'RMS level (mean SPL) = ' + str(RMSlev) + ' dB re ' + str(pref) + '$\mu$Pa')
                 print(r'Median SPL = ' + str(medlev) + ' dB re ' + str(pref) + '$\mu$Pa')
                 print(r'Mode SPL = ' + str(modelev) + ' dB re ' + str(pref) + ' $\mu$Pa')
            else:
                 print(r'Relative normalised RMS SPL (mean SPL) = ' + str(RMSlev) + ' dB')
                 print(r'Relative normalised median SPL = ' + str(medlev) + ' dB')
                 print(r'Relative normalised mode SPL = ' + str(modelev) + ' dB')
   
            tind = t[2] - t[1]
            SEL = 10*log10( tind*sum( 10**(A/10) ) )
            if ( calib == 1 ):
                 print(r'SEL = ' + str(SEL) + ' dB re ' + str(pref) + '$\mu$Pa$^2$ s.') 
                 print('Note: for SEL measurements, set window length to 1 s and window overlap to 0 percent.')
            else:
                 print(r'Relative normalised SEL = ' + str(SEL) + ' dB.') 
                 print('Note: for SEL measurements, set window length to 1 s and window overlap to 0 percent.')
#======================================================================
## Plot
       print('Plotting...')
       figure() # initialise figure
#======================================================================
       if ( atype != 'Broadband' ):
          if ( linlog == 0 ):
             xscale('log')
             if ( M > 1000 ):
                  pcolormesh(X,Y,d,cmap='viridis',edgecolors='face',shading='auto',vmin=0,vmax=0.05) # SPD
                  cb = colorbar()
                  cb.set_label('Empirical Probability Density',fontsize=14)
             semilogx(f,p[:,-1],'k',linewidth=2,label='99%') # percentiles
             semilogx(f,p[:,-5],color=[0.1, 0.1, 0.1],linewidth=2,label='95%')
             semilogx(f,p[:,49],color=[0.2, 0.2, 0.2],linewidth=2,label='50%')
             semilogx(f,p[:, 4],color=[0.3, 0.3, 0.3],linewidth=2,label=' 5%')
             semilogx(f,p[:, 0],color=[0.4, 0.4, 0.4],linewidth=2,label=' 1%')
             semilogx(f,RMSlevel,'m',linewidth=2,label='RMS Level') # RMS Level
             xlim(f[0],f[-1])
             ylim(mindB,maxdB)
             legend(loc='best')
          elif ( linlog == 1 ):
             xscale('linear')
             if ( M > 1000 ):
                  pcolormesh(X,Y,d,cmap='viridis',shading='auto',vmin=0,vmax=0.05) # SPD
                  cb = colorbar()
                  cb.set_label('Empirical Probability Density',fontsize=14)
             plot(f,p[:,-1],'k',linewidth=2,label='99%') # percentiles
             plot(f,p[:,-5],color=[0.1, 0.1, 0.1],linewidth=2,label='95%')
             plot(f,p[:,49],color=[0.2, 0.2, 0.2],linewidth=2,label='50%')
             plot(f,p[:, 4],color=[0.3, 0.3, 0.3],linewidth=2,label=' 5%')
             plot(f,p[:, 0],color=[0.4, 0.4, 0.4],linewidth=2,label=' 1%')
             plot(f,RMSlevel,'m',linewidth=2,label='RMS Level') # RMS Level
             xlim(f[0],f[-1])
             ylim(mindB,maxdB)
             legend(loc='best')
          title('Noise level statistics of ' + fileName)
          xlabel('Frequency [ Hz ]',fontsize=14)
          if ( atype == 'PSD' ):
             if ( calib == 1 ):
                ylabel(r'PSD [ dB re ' + str(pref) + ' $\mu$Pa$^2$/Hz ]',fontsize=14)
             else:
                ylabel('Relative PSD [ dB ]',fontsize=14)
          elif ( atype == 'PowerSpec' ):
             if ( calib == 1 ):
                ylabel(r'Power spectrum [ dB re ' + str(pref) + ' $\mu$Pa ]',fontsize=14)
             else:
                ylabel('Relative power spectrum [ dB ]')
          elif ( ( atype == 'TOL' ) or ( atype == 'TOLf' ) ):
             if ( calib == 1 ):
                ylabel(r'1/3-octave SPL [ dB re ' + str(pref) + ' $\mu$Pa ]',fontsize=14)
             else:
                ylabel('Relative 1/3-octave SPL [ dB ]',fontsize=14)
#======================================================================
       else:
             p = zeros(101)
             x = linspace(0,1,101)
             for i in range(101):
                 p[i] = percentile(A,i)
             RMSlev = 10*log10(  mean( 10**(A/10) ) )
             medlev = 10*log10(median( 10**(A/10) ) )
             modelev = stats.mode( round_(10*A)/10, axis=None )[0][0]
             plot(p,x,'k',label='CDF') 
             plot([RMSlev , RMSlev ],[0, 1],'m',label='RMS level')
             plot([medlev , medlev ],[0, 1],'g',label='Median')
             plot([modelev, modelev],[0, 1],'b',label='Mode')
             legend(loc='best')
             ylabel('Cumulative Distribution Function',fontsize=14)
             if ( calib == 1 ):
                xlabel(r'Broadband SPL [ dB re ' + str(pref) + '$\mu$Pa ]',fontsize=14)
             else:
                xlabel('Relative SPL [ dB ]')
             title('CDF of broadband SPL for ' + fileName)
#======================================================================
       if ( ( atype != 'Broadband') and ( M < 1000 ) ):
          print('Too few time segments (M = ' + str(M) + ', i.e. < 1000) for SPD analysis:') 
          print('for SPD, use a longer file or shorter time segment length (N).')
#======================================================================
#Exporting variable for future use:          
       mdic = {"A": A, "f": f, "t": t}
       savemat("Aft.mat", mdic)
#======================================================================
    show()
    print('Done.')
    return 
