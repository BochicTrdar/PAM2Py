# PAM2Py Python ToolBox
# Version 2.1
# JONAS Project 
# Written by Orlando Camargo Rodriguez
# Based on PAMGuide.m by Nathan D. Merchant
# Faro, Seg 14 Mar 2022 12:32:25 WET 
#==========================================================================
# Don't like it? Don't use it...
#==========================================================================

# YUP, I DO NOT USE NAMESPACES!!!!!!!
# TKinter stuff:
from tkinter import *    # standard binding to Tk
from tkinter import ttk  # Python's binding to the newer "themed widgets" 
from tkinter import filedialog
from tkinter import messagebox
# Numpy and Scipy stuff:
from numpy import *
from scipy.io import loadmat
# FLAC, WAV support: 
import soundfile as sf
# Matplotlib: 
from matplotlib.pyplot import *
# OS stuff
import os
# PAMGuide stuff: 
from PG_Func   import *
from write_edf import *
#======================================================================
#======================================================================
# GUI for the processing of experimental data:
#======================================================================
#======================================================================
def gui_experimental():
    Data_Type.set('Experimental')
    jge.set( jge.get() + 1 ) 
    ngui = jge.get()
    if ( ngui > 1 ): 
       messagebox.showinfo("Oops", 'Window already open.')        
    else:
       GExperimental = Toplevel(root, borderwidth=10, relief=GROOVE)
       GExperimental.title("Experimental Data")
       GExperimental.grab_set()
       ttk.Label(GExperimental, text='Select File Type:', style='TE.TLabel').grid(column=1,row=1)
       ttk.Radiobutton(GExperimental, text="FLAC", style='RE2.TRadiobutton', variable=sndtype, value='FLAC').grid(column=1, row=2)
       ttk.Radiobutton(GExperimental, text="WAV" , style='RE2.TRadiobutton', variable=sndtype, value='WAV' ).grid(column=1, row=3)
       ttk.Button(GExperimental, text="Single File", style='GE.TButton', command=gui_experimentals).grid(column=1, row=4, padx=5, pady=5)
       ttk.Button(GExperimental, text="Batch", style='GE.TButton', command=gui_experimentala).grid(column=1, row=5, padx=5, pady=5)
       ttk.Button(GExperimental, text="Close", style='CB.TButton', command=lambda:[jge.set(0),GExperimental.grab_release(),GExperimental.destroy()]).grid(column=1, row=6, padx=5, pady=5)
    return
#======================================================================
#======================================================================
# GUI for the processing of experimental data (single file):
#======================================================================
#======================================================================
def gui_experimentals():    
    jges.set( jges.get() + 1 ) 
    ngui = jges.get()
    if ( ngui > 1 ): 
       messagebox.showinfo("Oops", 'Window already open.')
    else:
       GExperimentalS = Toplevel(root, borderwidth=10, relief=GROOVE)
       GExperimentalS.title("Experimental Data - Single File")
       GExperimentalS.grab_set()
       ttk.Button(GExperimentalS, text="Select File", style='GE.TButton', command=infosnd).grid(column=1, row=1, padx=5, pady=5)
       ttk.Button(GExperimentalS, text="Calibration", style='GE.TButton', command=gui_calib).grid(column=1, row=2, padx=5, pady=5)
       ttk.Button(GExperimentalS, text="Analysis", style='GE.TButton', command=gui_analysis).grid(column=1, row=3, padx=5, pady=5)
       ttk.Button(GExperimentalS, text="RUN", style='RB.TButton', command=run_analysis).grid(column=1, row=4, padx=5,pady=5)
       ttk.Button(GExperimentalS, text="Write CSV/EDF?", style='CB.TButton', command=gui_writeout).grid(column=1, row=5, padx=5,pady=5)
       ttk.Button(GExperimentalS, text="Close", style='CB.TButton', command=lambda:[jges.set(0),GExperimentalS.grab_release(),GExperimentalS.destroy()]).grid(column=1, row=6, padx=5, pady=5)
    return
#======================================================================
#======================================================================
# GUI for the processing of experimental data (batch):
#======================================================================
#======================================================================
def gui_experimentala():
    jgea.set( jgea.get() + 1 ) 
    ngui = jgea.get()
    if ( ngui > 1 ): 
       messagebox.showinfo("Oops", 'Window already open.')
    else:
       GExperimentalA = Toplevel(root, borderwidth=10, relief=GROOVE)
       GExperimentalA.title("Experimental Data - Batch")
       GExperimentalA.grab_set()
       ttk.Button(GExperimentalA, text="Select Directory", style='GE.TButton', command=infodir).grid(column=1, row=1, padx=5, pady=5)
       ttk.Button(GExperimentalA, text="Calibration", style='GE.TButton', command=gui_calib).grid(column=1, row=2, padx=5, pady=5)
       ttk.Button(GExperimentalA, text="Analysis", style='GE.TButton', command=gui_analysis).grid(column=1, row=3, padx=5, pady=5)
       ttk.Button(GExperimentalA, text="RUN", style='RB.TButton', command=run_analysis).grid(column=1, row=4, padx=5,pady=5)
       ttk.Button(GExperimentalA, text="Write CSV/EDF?", style='CB.TButton', command=gui_writeout).grid(column=1, row=5, padx=5,pady=5)
       ttk.Button(GExperimentalA, text="Close", style='CB.TButton', command=lambda:[jgea.set(0),GExperimentalA.grab_release(),GExperimentalA.destroy()]).grid(column=1, row=6, padx=5, pady=5)
    return
#======================================================================
#======================================================================
# GUI for the processing of numerical data:
#======================================================================
#======================================================================
def gui_numerical():
    Data_Type.set('Numerical')
    CSVOUT.set('No')
    EDFOUT.set('Yes')
    jgn.set( jgn.get() + 1 ) 
    ngui = jgn.get()    
    if ( ngui > 1 ): 
       messagebox.showinfo("Oops", 'Window already open.')        
    else:
       GNumerical = Toplevel(root, borderwidth=10, relief=GROOVE)
       GNumerical.title("Numerical Data")
       GNumerical.grab_set()
       ttk.Button(GNumerical, text="Select File", style='GE.TButton', command=infomat).grid(column=1, row=1, padx=5, pady=5)
       ttk.Button(GNumerical, text="Plot", style='GE.TButton', command=plotmat).grid(column=1, row=2, padx=5, pady=5)
       ttk.Button(GNumerical, text="Write EDF?", style='CB.TButton', command=writeout).grid(column=1, row=5, padx=5,pady=5)
       ttk.Button(GNumerical, text="Close", style='CB.TButton', command=lambda:[jgn.set(0),GNumerical.grab_release(),GNumerical.destroy()]).grid(column=1, row=6, padx=5, pady=5)
    return
#======================================================================
#======================================================================
# GUI for the writing of MetaData:
#======================================================================
#======================================================================
def gui_meta():
    jmd.set( jmd.get() + 1 ) 
    ngui = jmd.get()    
    if ( ngui > 1 ): 
       messagebox.showinfo("Oops", 'Window already open.')        
    else:
       GMeta = Toplevel(root, borderwidth=10, relief=GROOVE)
       GMeta.title("Write MetaData")
       GMeta.grab_set()
       ttk.Button(GMeta, text="Experimental", style='GE.TButton', command=gui_metaexp).grid(column=1, row=1, padx=5, pady=5)
       ttk.Button(GMeta, text="Numerical"   , style='GE.TButton', command=gui_metanum).grid(column=1, row=2, padx=5, pady=5)
       ttk.Button(GMeta, text="Close", style='CB.TButton', command=lambda:[jmd.set(0),GMeta.grab_release(),GMeta.destroy()]).grid(column=1, row=3, padx=5, pady=5)
    return
#======================================================================
# Stuff called by the GUIs:
#======================================================================
# GUI to input calibration parameters:
def gui_calib():
    jcal.set( jcal.get() + 1 ) 
    ngui = jcal.get()
    if ( ngui > 1 ): 
       messagebox.showinfo("Oops", 'Window already open.')        
    else:
       Gcalib = Toplevel(root, borderwidth=10, relief=GROOVE)
       Gcalib.title("Calibration")
       Gcalib.grab_set()
       # Labels, column 1:
       ttk.Label(Gcalib,text='Environment:'           ).grid(column=1,row=1)
       ttk.Label(Gcalib,text='Calibration Type:'      ).grid(column=1,row=2)
       ttk.Label(Gcalib,text='System Sensitivity:'    ).grid(column=1,row=3)
       ttk.Label(Gcalib,text='Transducer Sensitivity:').grid(column=1,row=4)
       ttk.Label(Gcalib,text='Gain:'                  ).grid(column=1,row=5)
       ttk.Label(Gcalib,text='ADC volts:'             ).grid(column=1,row=6)
       # Labels, column 3:
       ttk.Label(Gcalib,text='dB re 1 V / Pa').grid(column=3,row=3)
       ttk.Label(Gcalib,text='dB'            ).grid(column=3,row=4)
       ttk.Label(Gcalib,text='dB'            ).grid(column=3,row=5)
       ttk.Label(Gcalib,text='V 0-peak'      ).grid(column=3,row=6)
       # Comboboxes, column 2:
       calibration = ttk.Combobox(Gcalib, width=30, textvariable=Envi)
       calibration['values'] = ('Air','Water') 
       calibration.grid(column =2, row =1)
       caltype = ttk.Combobox(Gcalib, width=30, textvariable=Ctype)
       caltype['values'] = ('None', 'EE', 'RC', 'TS')
       caltype.grid(column =2, row =2)
       # Entries, column 2:
       ttk.Entry(Gcalib,textvariable=SI  ,width=30).grid(column=2,row=3)
       ttk.Entry(Gcalib,textvariable=MH  ,width=30).grid(column=2,row=4)
       ttk.Entry(Gcalib,textvariable=GG  ,width=30).grid(column=2,row=5)
       ttk.Entry(Gcalib,textvariable=VADC,width=30).grid(column=2,row=6)
       # Button, column 1:
       ttk.Button(Gcalib, text="Close", style ='CB.TButton', command=lambda:[jcal.set(0),Gcalib.grab_release(),Gcalib.destroy()]).grid(column=2, row=7, padx=5, pady=5)
    return
#======================================================================
# GUI to input analysis options:
def gui_analysis():
    jan.set( jan.get() + 1 ) 
    ngui = jan.get()
    if ( ngui > 1 ): 
       messagebox.showinfo("Oops", 'Window already open.')        
    else:
       Ganalysis = Toplevel(root, borderwidth=10, relief=GROOVE)
       Ganalysis.title("Analysis")
       Ganalysis.grab_set()
       # Labels, column 1:
       ttk.Label(Ganalysis,text='Analysis Type:'   ).grid(column=1,row=1)
       ttk.Label(Ganalysis,text='Window Type:'     ).grid(column=1,row=2)
       ttk.Label(Ganalysis,text='Plot Type:'       ).grid(column=1,row=3)
       ttk.Label(Ganalysis,text='Frequency Scale:' ).grid(column=1,row=4)
       ttk.Label(Ganalysis,text='Window Overlap:'  ).grid(column=1,row=5)
       ttk.Label(Ganalysis,text='Window Length:'   ).grid(column=1,row=6)
       ttk.Label(Ganalysis,text='Low Freq. limit:' ).grid(column=1,row=7)
       ttk.Label(Ganalysis,text='High Freq. limit:').grid(column=1,row=8)
       ttk.Label(Ganalysis,text='Welch factor:'    ).grid(column=1,row=9)
       # Labels, column 3:
       ttk.Label(Ganalysis,text='%' ).grid(column=3,row=5)
       ttk.Label(Ganalysis,text='s' ).grid(column=3,row=6)
       ttk.Label(Ganalysis,text='Hz').grid(column=3,row=7)
       ttk.Label(Ganalysis,text='Hz').grid(column=3,row=8)
       # Comboboxes, column 2:
       anatype = ttk.Combobox(Ganalysis, width=30, textvariable=Atype)
       anatype['values'] = ('PSD','TOL','TOLf','Broadband','Waveform') 
       anatype.grid(column =2, row =1)
       wintype = ttk.Combobox(Ganalysis, width=30, textvariable=Winname)
       wintype['values'] = ('None', 'Hann', 'Hamming', 'Blackman')
       wintype.grid(column =2, row =2)
       plttype = ttk.Combobox(Ganalysis, width=30, textvariable=Plottype)
       plttype['values'] = ('Time', 'Stats', 'Both')
       plttype.grid(column =2, row =3)
       fscale = ttk.Combobox(Ganalysis, width=30, textvariable=Linlog)
       fscale['values'] = ('Logarithmic','Linear')
       fscale.grid(column =2, row =4)
       # Entries, column 2:
       ttk.Entry(Ganalysis,textvariable=Wover  ,width=30).grid(column=2,row=5)
       ttk.Entry(Ganalysis,textvariable=Wlength,width=30).grid(column=2,row=6)
       ttk.Entry(Ganalysis,textvariable=Lcut   ,width=30).grid(column=2,row=7)
       ttk.Entry(Ganalysis,textvariable=Hcut   ,width=30).grid(column=2,row=8)
       ttk.Entry(Ganalysis,textvariable=Welch  ,width=30).grid(column=2,row=9)  
       # Button, column 1:
       ttk.Button(Ganalysis, text="Close", style ='CB.TButton', command=lambda:[jan.set(0),Ganalysis.grab_release(),Ganalysis.destroy()]).grid(column=2, row=10, padx=5, pady=5)
    return
#======================================================================
# GUI to write CVS/EDF:
def gui_writeout():
    jwo.set( jwo.get() + 1 ) 
    ngui = jwo.get()
    if ( ngui > 1 ): 
       messagebox.showinfo("Oops", 'Window already open.')        
    else:
       c = os.path.isfile('Aft.mat')
       if ( c == True ):
          Gwrite = Toplevel(root, borderwidth=10, relief=GROOVE)
          Gwrite.title("Write CSV/EDF?")
          Gwrite.grab_set()
          ttk.Label(Gwrite, text='Select Output Type:', style='TE.TLabel').grid(column=1, row=1)
          C1 = ttk.Checkbutton(Gwrite, text = "CSV", style='CB2.TCheckbutton', variable=CSVOUT, onvalue='Yes', offvalue='No').grid(column=1, row=2)
          C2 = ttk.Checkbutton(Gwrite, text = "EDF", style='CB2.TCheckbutton', variable=EDFOUT, onvalue='Yes', offvalue='No').grid(column=1, row=3)
          ttk.Button(Gwrite, text="Write", style ='CB.TButton', command=writeout).grid(column=1, row=4, padx=5, pady=5)
          ttk.Button(Gwrite, text="Close", style ='CB.TButton', command=lambda:[jwo.set(0),Gwrite.grab_release(),Gwrite.destroy()]).grid(column=1, row=5, padx=5, pady=5)
       else: 
          messagebox.showinfo("Oops...", 'Run Analysis first (except Waveform option)')
    return
#======================================================================
# GUI to create numerical metadata:
def gui_metanum():    
    Data_Type.set('Numerical')
    jmdn.set( jmdn.get() + 1 ) 
    ngui = jmdn.get()
    if ( ngui > 1 ): 
       messagebox.showinfo("Oops", 'Window already open.')        
    else:
       Gmetanum = Toplevel(root, borderwidth=10, relief=GROOVE)
       Gmetanum.title("Numerical Metadata")
       Gmetanum.grab_set()
       ttk.Label(Gmetanum,text='Filename:'                    ).grid(column=1,row=1)
       ttk.Entry(Gmetanum,textvariable=metfile,       width=30).grid(column=2,row=1)
       ttk.Label(Gmetanum,text='Format Version:'              ).grid(column=1,row=2)
       ttk.Entry(Gmetanum,textvariable=Format_Version,width=30).grid(column=2,row=2)
       ttk.Label(Gmetanum,text='Author:'                      ).grid(column=1,row=3)
       ttk.Entry(Gmetanum,textvariable=Author,        width=30).grid(column=2,row=3)
       ttk.Label(Gmetanum,text='Institution:'                 ).grid(column=1,row=4)
       ttk.Entry(Gmetanum,textvariable=Institution,   width=30).grid(column=2,row=4)
       ttk.Label(Gmetanum,text='Country Code:'                ).grid(column=1,row=5)
       ttk.Entry(Gmetanum,textvariable=Country_Code,  width=30).grid(column=2,row=5)
       ttk.Label(Gmetanum,text='Contact:'                     ).grid(column=1,row=6)
       ttk.Entry(Gmetanum,textvariable=Contact,       width=30).grid(column=2,row=6)
       ttk.Label(Gmetanum,text='Start Date (YYYYMMDD):'       ).grid(column=1,row=7)
       ttk.Entry(Gmetanum,textvariable=Start_Date,    width=30).grid(column=2,row=7)
       ttk.Label(Gmetanum,text='End Date (YYYYMMDD):'         ).grid(column=1,row=8)
       ttk.Entry(Gmetanum,textvariable=End_Date,      width=30).grid(column=2,row=8)
       ttk.Label(Gmetanum,text='Creation Date (YYYYMMDD):'    ).grid(column=1,row=9)
       ttk.Entry(Gmetanum,textvariable=Creation_Date, width=30).grid(column=2,row=9)
       ttk.Label(Gmetanum,text='Purpose:'                     ).grid(column=1,row=10)
       ttk.Entry(Gmetanum,textvariable=Purpose,       width=30).grid(column=2,row=10)
       ttk.Label(Gmetanum,text='Data UUID:'                   ).grid(column=1,row=11)
       ttk.Entry(Gmetanum,textvariable=Data_Uuid,     width=30).grid(column=2,row=11)
       ttk.Label(Gmetanum,text='Data Type:'                   ).grid(column=3,row=2)
       ttk.Label(Gmetanum,text='Numerical'                    ).grid(column=4,row=2)
       ttk.Label(Gmetanum,text='Comments:'                    ).grid(column=3,row=3)
       ttk.Entry(Gmetanum,textvariable=Comments,      width=30).grid(column=4,row=3)
       ttk.Label(Gmetanum,text='AIS Database:'                ).grid(column=3,row=4)
       ttk.Entry(Gmetanum,textvariable=AIS_DB,        width=30).grid(column=4,row=4)
       ttk.Label(Gmetanum,text='Source Levels:'               ).grid(column=3,row=5)
       ttk.Entry(Gmetanum,textvariable=Source_Levels, width=30).grid(column=4,row=5)
       ttk.Label(Gmetanum,text='Bathymetry Database:'         ).grid(column=3,row=6)
       ttk.Entry(Gmetanum,textvariable=Bathy_DB,      width=30).grid(column=4,row=6)
       ttk.Label(Gmetanum,text='Temperature Database:'        ).grid(column=3,row=7)
       ttk.Entry(Gmetanum,textvariable=Temperature_DB,width=30).grid(column=4,row=7)
       ttk.Label(Gmetanum,text='Salinity Database:'           ).grid(column=3,row=8)
       ttk.Entry(Gmetanum,textvariable=Salinity_DB,   width=30).grid(column=4,row=8)
       ttk.Label(Gmetanum,text='SSP Model:'                   ).grid(column=3,row=9)
       ttk.Entry(Gmetanum,textvariable=SSP_Model,     width=30).grid(column=4,row=9)
       ttk.Label(Gmetanum,text='Propagation Model:'              ).grid(column=3,row=10)
       ttk.Entry(Gmetanum,textvariable=Propagation_Model,width=30).grid(column=4,row=10)
       ttk.Label(Gmetanum,text='Data Calibration:'               ).grid(column=3,row=11)
       ttk.Entry(Gmetanum,textvariable=Data_Calibration, width=30).grid(column=4,row=11)
       ttk.Button(Gmetanum, text="Write", style='CB.TButton', command=writenum).grid(column=3, row=12, padx=5, pady=5)
       ttk.Button(Gmetanum, text="Close", style='CB.TButton', command=lambda:[jmdn.set(0),Gmetanum.grab_release(),Gmetanum.destroy()]).grid(column=4, row=12, padx=5, pady=5)
    return
#======================================================================
# GUI to create experimental metadata:
def gui_metaexp():
    Data_Type.set('Experimental')
    jmde.set( jmde.get() + 1 ) 
    ngui = jmde.get()
    if ( ngui > 1 ): 
       messagebox.showinfo("Oops", 'Window already open.')        
    else:
       Gmetaexp = Toplevel(root, borderwidth=10, relief=GROOVE)
       Gmetaexp.title("Experimental Metadata")
       Gmetaexp.grab_set()
       Data_Type.set('Experimental')
       ttk.Label(Gmetaexp,text='Filename:'                    ).grid(column=1,row=1)
       ttk.Entry(Gmetaexp,textvariable=metfile,       width=30).grid(column=2,row=1)
       ttk.Label(Gmetaexp,text='Format Version:'              ).grid(column=1,row=2)
       ttk.Entry(Gmetaexp,textvariable=Format_Version,width=30).grid(column=2,row=2)
       ttk.Label(Gmetaexp,text='Author:'                      ).grid(column=1,row=3)
       ttk.Entry(Gmetaexp,textvariable=Author,        width=30).grid(column=2,row=3)
       ttk.Label(Gmetaexp,text='Institution:'                 ).grid(column=1,row=4)
       ttk.Entry(Gmetaexp,textvariable=Institution,   width=30).grid(column=2,row=4)
       ttk.Label(Gmetaexp,text='Country Code:'                ).grid(column=1,row=5)
       ttk.Entry(Gmetaexp,textvariable=Country_Code,  width=30).grid(column=2,row=5)
       ttk.Label(Gmetaexp,text='Contact:'                     ).grid(column=1,row=6)
       ttk.Entry(Gmetaexp,textvariable=Contact,       width=30).grid(column=2,row=6)
       ttk.Label(Gmetaexp,text='Start Date (YYYYMMDD):'       ).grid(column=1,row=7)
       ttk.Entry(Gmetaexp,textvariable=Start_Date,    width=30).grid(column=2,row=7)
       ttk.Label(Gmetaexp,text='End Date (YYYYMMDD):'         ).grid(column=1,row=8)
       ttk.Entry(Gmetaexp,textvariable=End_Date,      width=30).grid(column=2,row=8)
       ttk.Label(Gmetaexp,text='Creation Date (YYYYMMDD):'    ).grid(column=1,row=9)
       ttk.Entry(Gmetaexp,textvariable=Creation_Date, width=30).grid(column=2,row=9)
       ttk.Label(Gmetaexp,text='Purpose:'                     ).grid(column=1,row=10)
       ttk.Entry(Gmetaexp,textvariable=Purpose,       width=30).grid(column=2,row=10)
       ttk.Label(Gmetaexp,text='Data UUID:'                   ).grid(column=1,row=11)
       ttk.Entry(Gmetaexp,textvariable=Data_Uuid,     width=30).grid(column=2,row=11)
       ttk.Label(Gmetaexp,text='Data Type:'                   ).grid(column=1,row=12)
       ttk.Label(Gmetaexp,text='Experimental'                 ).grid(column=2,row=12)
       ttk.Label(Gmetaexp,text='Comments:'                    ).grid(column=1,row=13)
       ttk.Entry(Gmetaexp,textvariable=Comments,      width=30).grid(column=2,row=13)
       ttk.Label(Gmetaexp,text='Expsetup:'                    ).grid(column=1,row=14)
       ttk.Entry(Gmetaexp,textvariable=Expsetup,      width=30).grid(column=2,row=14)
       ttk.Label(Gmetaexp,text='Recorder Manufacturer:'       ).grid(column=1,row=15)
       ttk.Entry(Gmetaexp,text=RecorderMa,            width=30).grid(column=2,row=15)
       ttk.Label(Gmetaexp,text='Recorder Serial Number:'      ).grid(column=1,row=16)
       ttk.Entry(Gmetaexp,textvariable=RecorderSN,    width=30).grid(column=2,row=16)
       ttk.Label(Gmetaexp,text='Recorder Model:'              ).grid(column=1,row=17)
       ttk.Entry(Gmetaexp,textvariable=RecorderMo,    width=30).grid(column=2,row=17)
       ttk.Label(Gmetaexp,text='Builtin Hydrophone:'          ).grid(column=1,row=18)
       ttk.Entry(Gmetaexp,textvariable=Builtin,       width=30).grid(column=2,row=18)
       ttk.Label(Gmetaexp,text='Hydrophone Manufacturer:'     ).grid(column=1,row=19)
       ttk.Entry(Gmetaexp,textvariable=HydroMa,       width=30).grid(column=2,row=19)
       ttk.Label(Gmetaexp,text='Hydrophone Sensitivity:'      ).grid(column=1,row=20)
       ttk.Entry(Gmetaexp,text=HydroS,                width=30).grid(column=2,row=20)
       ttk.Label(Gmetaexp,text='Hydrophone Serial Number:'    ).grid(column=1,row=21)
       ttk.Entry(Gmetaexp,textvariable=HydroSN,       width=30).grid(column=2,row=21)
       ttk.Label(Gmetaexp,text='Hydrophone Model:'            ).grid(column=1,row=22)
       ttk.Entry(Gmetaexp,textvariable=HydroMo,       width=30).grid(column=2,row=22)
       ttk.Label(Gmetaexp,text='Average Time (s):'            ).grid(column=3,row=2)
       ttk.Entry(Gmetaexp,textvariable=AVtime ,       width=30).grid(column=4,row=2)
       ttk.Label(Gmetaexp,text='Calibration Datetime:'        ).grid(column=3,row=3)
       ttk.Entry(Gmetaexp,text=CalibD,                width=30).grid(column=4,row=3)
       ttk.Label(Gmetaexp,text='Calibration Factor:'          ).grid(column=3,row=4)
       ttk.Entry(Gmetaexp,textvariable=CalibF,        width=30).grid(column=4,row=4)
       ttk.Label(Gmetaexp,text='Calibration Procedure:'       ).grid(column=3,row=5)
       ttk.Entry(Gmetaexp,textvariable=CalibP,        width=30).grid(column=4,row=5)
       ttk.Label(Gmetaexp,text='Reference Frequencies:'       ).grid(column=3,row=6)
       ttk.Entry(Gmetaexp,textvariable=RefFreq,       width=30).grid(column=4,row=6)
       ttk.Label(Gmetaexp,text='Calibration Frequency Count:' ).grid(column=3,row=7)
       ttk.Entry(Gmetaexp,textvariable=CalibCount,    width=30).grid(column=4,row=7)
       ttk.Label(Gmetaexp,text='Longitude:'                   ).grid(column=3,row=8)
       ttk.Entry(Gmetaexp,textvariable=Longitude,     width=30).grid(column=4,row=8)
       ttk.Label(Gmetaexp,text='Latitude:'                    ).grid(column=3,row=9)
       ttk.Entry(Gmetaexp,textvariable=Latitude,      width=30).grid(column=4,row=9)
       ttk.Label(Gmetaexp,text='Depth (m):'                   ).grid(column=3,row=10)
       ttk.Entry(Gmetaexp,textvariable=Depth,         width=30).grid(column=4,row=10)
       ttk.Label(Gmetaexp,text='Frequency Count:'             ).grid(column=3,row=11)
       ttk.Entry(Gmetaexp,textvariable=FreqCount,     width=30).grid(column=4,row=11)
       ttk.Label(Gmetaexp,text='Frequency Band Definition:'   ).grid(column=3,row=12)
       ttk.Entry(Gmetaexp,textvariable=FreqBand,      width=30).grid(column=4,row=12)
       ttk.Label(Gmetaexp,text='Time Duty On:'                ).grid(column=3,row=13)
       ttk.Entry(Gmetaexp,textvariable=TimeDO,        width=30).grid(column=4,row=14)
       ttk.Label(Gmetaexp,text='Time Duty Off:'               ).grid(column=3,row=14)
       ttk.Entry(Gmetaexp,textvariable=TimeDF,        width=30).grid(column=4,row=14)
       ttk.Label(Gmetaexp,text='Hydrophone Count:'            ).grid(column=3,row=15)
       ttk.Entry(Gmetaexp,textvariable=HydroCount,    width=30).grid(column=4,row=15)
       ttk.Label(Gmetaexp,text='Percentile Count:'            ).grid(column=3,row=16)
       ttk.Entry(Gmetaexp,textvariable=PercCount,     width=30).grid(column=4,row=16)
       ttk.Label(Gmetaexp,text='Percentile List:'             ).grid(column=3,row=17)
       ttk.Entry(Gmetaexp,textvariable=PercList,      width=30).grid(column=4,row=17)
#      Buttons:
       ttk.Button(Gmetaexp, text="Write", style='CB.TButton', command=writeexp).grid(column=4, row=22, padx=5, pady=5)
       ttk.Button(Gmetaexp, text="Close", style='CB.TButton', command=lambda:[jmde.set(0),Gmetaexp.grab_release(),Gmetaexp.destroy()]).grid(column=4, row=23, padx=5, pady=5)
    return
#======================================================================
# Function to write the experimental metadata file:
def writeexp(*args):
    dfile = metfile.get()
    Data_Type.set('Experimental')
    if ( dfile == 'Nothing selected...' ):
       messagebox.showinfo("Oops", 'Specify a filename first...') 
    else:
       metadatafile = open(dfile, "w") # Experimental metadata: 37 parameters
       metadatafile.write(Format_Version.get()+'\n') # 1
       metadatafile.write(        Author.get()+'\n') # 2
       metadatafile.write(   Institution.get()+'\n') # 3
       metadatafile.write(  Country_Code.get()+'\n') # 4
       metadatafile.write(       Contact.get()+'\n') # 5
       metadatafile.write(    Start_Date.get()+'\n') # 6
       metadatafile.write(      End_Date.get()+'\n') # 7
       metadatafile.write( Creation_Date.get()+'\n') # 8
       metadatafile.write(       Purpose.get()+'\n') # 9
       metadatafile.write(     Data_Uuid.get()+'\n') # 10
       metadatafile.write(     Data_Type.get()+'\n') # 11
       metadatafile.write(      Comments.get()+'\n') # 12
       metadatafile.write(      Expsetup.get()+'\n') # 13
       metadatafile.write(    RecorderMa.get()+'\n') # 14 
       metadatafile.write(    RecorderSN.get()+'\n') # 15
       metadatafile.write(    RecorderMo.get()+'\n') # 16
       metadatafile.write(       Builtin.get()+'\n') # 17
       metadatafile.write(       HydroMa.get()+'\n') # 18
       metadatafile.write(        HydroS.get()+'\n') # 19
       metadatafile.write(       HydroSN.get()+'\n') # 20
       metadatafile.write(       HydroMo.get()+'\n') # 21
       metadatafile.write(        AVtime.get()+'\n') # 22
       metadatafile.write(        CalibD.get()+'\n') # 23
       metadatafile.write(        CalibF.get()+'\n') # 24
       metadatafile.write(        CalibP.get()+'\n') # 25
       metadatafile.write(       RefFreq.get()+'\n') # 26
       metadatafile.write(    CalibCount.get()+'\n') # 27
       metadatafile.write(     Longitude.get()+'\n') # 28
       metadatafile.write(      Latitude.get()+'\n') # 29
       metadatafile.write(         Depth.get()+'\n') # 30
       metadatafile.write(     FreqCount.get()+'\n') # 31
       metadatafile.write(      FreqBand.get()+'\n') # 32
       metadatafile.write(        TimeDO.get()+'\n') # 33
       metadatafile.write(        TimeDF.get()+'\n') # 34
       metadatafile.write(    HydroCount.get()+'\n') # 35
       metadatafile.write(     PercCount.get()+'\n') # 36
       metadatafile.write(      PercList.get()+'\n') # 37
       metadatafile.close()
       messagebox.showinfo("Done:", 'Metadata written to ' + dfile)
    return
#======================================================================
# Function to write the numerical metadata file:
def writenum(*args):
    dfile = metfile.get()
    Data_Type.set('Numerical')    
    if ( dfile == 'Nothing selected...' ):
       messagebox.showinfo("Oops", 'Specify a filename first...') 
    else:
       metadatafile = open(dfile, "w") # Numerical metadata: 20 parameters
       metadatafile.write(Format_Version.get()+'\n') # 1
       metadatafile.write(        Author.get()+'\n') # 2
       metadatafile.write(   Institution.get()+'\n') # 3
       metadatafile.write(  Country_Code.get()+'\n') # 4
       metadatafile.write(       Contact.get()+'\n') # 5
       metadatafile.write(    Start_Date.get()+'\n') # 6
       metadatafile.write(      End_Date.get()+'\n') # 7
       metadatafile.write( Creation_Date.get()+'\n') # 8
       metadatafile.write(       Purpose.get()+'\n') # 9
       metadatafile.write(     Data_Uuid.get()+'\n') # 10
       metadatafile.write(     Data_Type.get()+'\n') # 11
       metadatafile.write(      Comments.get()+'\n') # 12
       metadatafile.write(        AIS_DB.get()+'\n') # 13
       metadatafile.write( Source_Levels.get()+'\n') # 14
       metadatafile.write(      Bathy_DB.get()+'\n') # 15
       metadatafile.write(Temperature_DB.get()+'\n') # 16
       metadatafile.write(   Salinity_DB.get()+'\n') # 17
       metadatafile.write(     SSP_Model.get()+'\n') # 18
       metadatafile.write(Propagation_Model.get()+'\n') # 19
       metadatafile.write( Data_Calibration.get()+'\n') # 20
       metadatafile.close()
       messagebox.showinfo("Done:", 'Metadata written to ' + dfile)
    return
#======================================================================
#======================================================================
#                              FUNCTIONS
#======================================================================
#======================================================================
# Function to open a GUI depending on the option:
def whichgui():
    thegui = gui2open.get()
    if ( thegui == 'GED' ):
       gui_experimental()
    elif ( thegui == 'GND' ):
       gui_numerical()
    elif ( thegui == 'GMD' ):
       gui_meta()
    else:
       messagebox.showerror("Oops", "Select an option first...")
    return
#======================================================================
# Function to run the analysis:
def run_analysis():
    ifile = sndfile.get()
    if ( ifile == 'Nothing selected...' ):
       messagebox.showerror("Error:", "Select a sound file first...")
    elif ( Hcut.get() == ' ' ):
       messagebox.showerror("Error:", "Specify a High Frequency...")
    else:
       atype    =    Atype.get()
       ctype    =    Ctype.get()
       plottype = Plottype.get()
       envi     =     Envi.get()
       winname  =  Winname.get()
       Si       = float(      SI.get() )
       Mh       = float(      MH.get() )
       G        = float(      GG.get() )
       vADC     = float(    VADC.get() )
       r        = float(   Wover.get() )*0.01
       wlength  = float( Wlength.get() )
       lcut     = float(    Lcut.get() )
       hcut     = float(    Hcut.get() )
       welch    = float(   Welch.get() )
       S = Linlog.get()
       if ( S == 'Logarithmic' ):
          linlog = 0
       else:
          linlog = 1
       PG_Func(ifile,atype,plottype,envi,ctype,Si,Mh,G,vADC,r,wlength,winname,lcut,hcut,welch,linlog)
    return
#======================================================================
# Function to select the sound file:
def infosnd(*args):
    sound_type = sndtype.get()
    thefile = 'Nothing selected...'
    if ( sound_type == '...' ): 
       messagebox.showinfo("Oops...", 'Select a file type first...')
    elif ( sound_type == 'FLAC' ):
       thefile = filedialog.askopenfilename(initialdir = "",title = "Select file", filetypes = (("FLAC files","*.flac"),("all files","*.*")))
    else:
       thefile = filedialog.askopenfilename(initialdir = "",title = "Select file", filetypes = (("WAV files","*.wav"),("all files","*.*")))
    sndfile.set(thefile)
    return
#======================================================================
# Function to select the directory:
def infodir(*args):
    thefile = filedialog.askdirectory(initialdir = "",title = "Select Directory")
    sndfile.set(thefile)
    mergefiles()
    return
#======================================================================
# Function to select the mat file:
def infomat(*args):
    thefile = filedialog.askopenfilename(initialdir = "",title = "Select file",filetypes = (("MAT files","*.mat"),("all files","*.*")))
    matfile.set(thefile)
    return
#======================================================================
# Function to merge files in the directory:
def mergefiles(*args):
    thefiles  = ''
    j = 0
    thedir  = sndfile.get()
    thetype = sndtype.get()
#   YUP, I prefer filextensions this way:
    if ( thetype == 'FLAC' ):
       thetype = 'flac'
    else:
       thetype = 'wav'

    x = os.listdir(thedir)
    for i in x:
        if i.endswith(thetype):
           j = j + 1
           thefiles = thefiles + ' ' + i    
    if ( j == 0 ):
       messagebox.showinfo("Oops", 'No sound files found...')
    elif ( j == 1 ):
       messagebox.showinfo("Oops", 'Only one file found...')
    else:
       list_of_files = thefiles.split()
       sampling_frequency = zeros(j)
       nchannels          = zeros(j)
       for i in range(j):
           thesignal,sampling_frequency[i] = sf.read( thedir + '/' + list_of_files[i] )
           nchannels[i] = len( thesignal.shape )
           thesignal = []
       cfreq = max( abs( diff( sampling_frequency ) ) )
       cchan = max( abs( diff( nchannels          ) ) )
       if ( cfreq != 0 ):
          messagebox.showinfo("Batch processing cancelled:", 'Sampling rate should be the same for all files...')
       elif ( cchan != 0 ):
          messagebox.showinfo("Batch processing cancelled:", 'Number of channels should be the same for all files...')
       else:
          Fs = int( sampling_frequency[0] )
          thefile = 'all.' + thetype  
          x = []        
          for i in range(j):
              thesignal,sampling_frequency[i] = sf.read( thedir + '/' + list_of_files[i] )
              x = append( x, thesignal )
              thesignal = []
          sf.write(thefile,x.astype(float32),Fs)
          sndfile.set(thefile)
    return
#======================================================================
# Function to plot the mat file:
def plotmat(*args):
    thefile = matfile.get()
    if ( thefile != 'Nothing selected...' ):
       matlab_data = loadmat(thefile,squeeze_me=True)
       frequency                 = matlab_data['frequency' ] # 7
       time                      = matlab_data['time'      ] # 8
       spl_values                = matlab_data['spl_values'] # 9
       percentile_list = matlab_data['percentile_list'] # 10
       percentile_count = len( percentile_list )
       cA         = spl_values[0,:].size 
       time_count = spl_values[:,0].size
       percentile_values = zeros((cA,percentile_count))
#      Calculate the percentiles:
       for i in range(percentile_count):
           percentile_values[:,i] = percentile(spl_values,percentile_list[i],axis=0)
       figure()
       yscale('log')
       pcolormesh(time,frequency,spl_values.transpose(),cmap='viridis',shading='auto')
       xlim(time[0],time[-1])
       ylim(frequency[0],frequency[-1])
       xlabel('Time [s]',fontsize=16)
       ylabel('Frequency [Hz]',fontsize=16)
       title('SPL values [dB]')
       colorbar()
       figure()
       for i in range(percentile_count):
           thelabel = str( percentile_list[i] ) + '%'
           plot(frequency,percentile_values[:,i],label=thelabel)
       xlabel('Frequency [Hz]',fontsize=16)
       title('Percentiles')
       legend(loc='best')
       show()
    else: 
       messagebox.showerror("Error:", "Select a *.mat file first...")
    return
#======================================================================
# Function to write the CSV and EDF files
# (the CSV is written only for experimental data):
def writeout(*args):
    writecsv = CSVOUT.get()
    writeedf = EDFOUT.get()
    fileextension = sndtype.get()
    mfile         = sndfile.get()
    if ( ( writecsv == 'No' ) and ( writeedf == 'No' ) ):
       messagebox.showinfo("Done.", 'Nothing to be written')
    if ( writecsv == 'Yes' ):
       matlab_data = loadmat('Aft.mat',squeeze_me=True)
       frequency   = matlab_data['f']
       time        = matlab_data['t']
       spl_values  = matlab_data['A']
       cA = frequency.size
       rA =      time.size
       data = zeros((rA+1,cA+1))
       data[1:,0] = time
       data[0,1:] = frequency
       data[1:,1:] = spl_values
       if ( fileextension == 'flac' ):
          csvfile = mfile[0:-4] + 'csv'
       else:
          csvfile = mfile[0:-3] + 'csv'
       savetxt(csvfile, data, delimiter=',', fmt='%f')
       csvmessage = 'Frequency, Time and SPL values written to ' + csvfile
       messagebox.showinfo("Done.", csvmessage )
    if ( writeedf == 'Yes' ):
       seldata = Data_Type.get()
       thefile = filedialog.askopenfilename(initialdir = "",title = "Select a Metadata File:",filetypes = (("Metadata files","*.met"),("all files","*.*")))
       metfile.set(thefile)
       messagebox.showinfo("Selected Metadata:", thefile)
# Check that the metadata file matches the Experimental/Numerical Case
       dfile = metfile.get()
       metadatafile = open(dfile, "r")
       for i in range(10):
           theline = metadatafile.readline()
       data_type = metadatafile.readline()
       data_type = data_type[0:-1].split()
       metadatafile.close()
       if ( data_type[0] != seldata ):
          mismatchinfo = 'Starting case: ' + seldata + ', Metadata: ' + data_type[0]
          messagebox.showinfo("Metadata mismatch...", mismatchinfo)         
       else:
          if ( fileextension == 'flac' ):
             hfile = mfile[0:-4] + 'h5'
          else:
             hfile = mfile[0:-3] + 'h5'
# Experimental Case:
          if ( data_type[0] == 'Experimental' ):
             metadatafile = open(dfile, "r") # Experimental metadata: 37 parameters
             format_version= metadatafile.readline(); format_version = format_version[0:-1] # 1
             author        = metadatafile.readline(); author         = author[        0:-1] # 2
             institution   = metadatafile.readline(); institution    = institution[   0:-1] # 3
             country_code  = metadatafile.readline(); country_code   = country_code[  0:-1] # 4
             contact       = metadatafile.readline(); contact        = contact[       0:-1] # 5
             start_date       = int( metadatafile.readline() ) # 6
             end_date         = int( metadatafile.readline() ) # 7
             date_of_creation = int( metadatafile.readline() ) # 8
             purpose      = metadatafile.readline(); purpose   = purpose[  0:-1] # 9
             data_uuid    = metadatafile.readline(); data_uuid = data_uuid[0:-1] # 10
             data_type    = metadatafile.readline(); data_type = data_type[0:-1] # 11
             comments     = metadatafile.readline(); comments  = comments[ 0:-1] # 12
             expsetup     = metadatafile.readline(); expsetup  = expsetup[ 0:-1] # 13
             recorder_manufacturer  = metadatafile.readline(); recorder_manufacturer  = recorder_manufacturer[ 0:-1] # 14
             recorder_serial_number = metadatafile.readline(); recorder_serial_number = recorder_serial_number[0:-1] # 15
             recorder_model         = metadatafile.readline(); recorder_model         = recorder_model[        0:-1] # 16
             builtin_hydrophone     = metadatafile.readline(); builtin_hydrophone     = builtin_hydrophone[    0:-1] # 17
             hydrophone_manufacturer= metadatafile.readline(); hydrophone_manufacturer= hydrophone_manufacturer[0:-1]# 18
             hydrophone_sensitivity = float( metadatafile.readline() ) # 19
             hydrophone_serial_number = metadatafile.readline(); hydrophone_serial_number = hydrophone_serial_number[0:-1] # 20
             hydrophone_model       = metadatafile.readline(); hydrophone_model = hydrophone_model[0:-1] # 21
             averaging_time         = float( metadatafile.readline() ) # 22
             calibration_datetime   =   int( metadatafile.readline() ) # 23
             calibration_factor     = float( metadatafile.readline() ) # 24
             calibration_procedure  = metadatafile.readline(); calibration_procedure = calibration_procedure[0:-1] # 25
             reference_frequencies  =   int( metadatafile.readline() ) # 26
             calibration_frequency_count = int( metadatafile.readline() ) # 27
             slongitudes            = metadatafile.readline().split() # 28
             slatitudes             = metadatafile.readline().split() # 29
             sdepths                = metadatafile.readline().split() # 30
             frequency_count        = int( metadatafile.readline() ) # 31
             frequency_band_definition = metadatafile.readline(); frequency_band_definition = frequency_band_definition[0:-1] # 32
             time_duty_on           = metadatafile.readline(); time_duty_on  = time_duty_on[ 0:-1] # 33
             time_duty_off          = metadatafile.readline(); time_duty_off = time_duty_off[0:-1] # 34
             hydrophone_count       = int( metadatafile.readline() ) # 35
             percentile_count       = int( metadatafile.readline() ) # 36
             splist                 = metadatafile.readline().split() # 37
             metadatafile.close()
#            Convert the lists of strings to lists of floats:
             depth     = [float(xi) for xi in sdepths     ]
             latitude  = [float(xi) for xi in slatitudes  ]
             longitude = [float(xi) for xi in slongitudes ]
             percentile_list = [float(xi) for xi in splist]
             percentile_count = len( percentile_list ) # Just in case... (yup, a list has length, not size)
#            The following are reference values and they are written but not 
#            used when information is extracted from the h5 file:
             total_number_of_grid_points = NaN
             ais_database           = 'AISHub - www.aishub.net'
             bathymetry_database    = 'GEBCO - www.gebco.net'
             temperature_database   = 'COPERNICUS - www.copernicus.eu'
             salinity_database      = 'COPERNICUS - www.copernicus.eu'
             sound_speed_profile_model = 'Mackenzie-nine-term equation'
             propagation_model         = 'KRAKEN'
             numeric_data_calibration = 'data uidn:xxxx-xxxx-xxxx-xxxx'
             source_levels          = [170.0, 120.0, 180.0]
             matlab_data = loadmat('Aft.mat',squeeze_me=True)
             frequency   = matlab_data['f']
             time        = matlab_data['t']
             spl_values  = matlab_data['A']
             cA         = spl_values[0,:].size 
             time_count = spl_values[:,0].size
             percentile_values = zeros((cA,percentile_count))
#            Calculate the percentiles:
             for i in range(percentile_count):
                 percentile_values[:,i] = percentile(spl_values,percentile_list[i],axis=0)
#======================================================================
# Numerical case (requires user's input about MAT file with data):
          else:
             mfile = matfile.get()
             hfile = mfile[0:-3] + 'h5'
             builtin_hydrophone     = 'N/A'
             calibration_procedure  = 'N/A'
             expsetup               = 'N/A'
             hydrophone_manufacturer= 'N/A'
             hydrophone_model       = 'N/A'
             hydrophone_serial_number='N/A'
             recorder_manufacturer  = 'N/A'
             recorder_model         = 'N/A'
             recorder_serial_number = 'N/A'
             time_duty_on           = 'N/A'
             time_duty_off          = 'N/A'
             averaging_time              = nan
             calibration_datetime        = nan
             calibration_factor          = nan
             calibration_frequency_count = nan
             reference_frequencies       = nan
             hydrophone_count            = nan
             hydrophone_sensitivity      = nan
             metadatafile = open(dfile, "r") # Numerical metadata: 20 parameters
             format_version= metadatafile.readline(); format_version = format_version[0:-1] # 1
             author        = metadatafile.readline(); author         = author[        0:-1] # 2
             institution   = metadatafile.readline(); institution    = institution[   0:-1] # 3
             country_code  = metadatafile.readline(); country_code   = country_code[  0:-1] # 4
             contact       = metadatafile.readline(); contact        = contact[       0:-1] # 5
             start_date       = int( metadatafile.readline() ) # 6
             end_date         = int( metadatafile.readline() ) # 7
             date_of_creation = int( metadatafile.readline() ) # 8
             purpose      = metadatafile.readline(); purpose   = purpose[  0:-1] # 9
             data_uuid    = metadatafile.readline(); data_uuid = data_uuid[0:-1] # 10
             data_type    = metadatafile.readline(); data_type = data_type[0:-1] # 11
             comments     = metadatafile.readline(); comments  = comments[ 0:-1] # 12
             ais_database = metadatafile.readline(); ais_database = ais_database[0:-1] # 13
             ssource_levels = metadatafile.readline().split() # 14
             bathymetry_database = metadatafile.readline(); bathymetry_database = bathymetry_database[ 0:-1] # 15
             temperature_database= metadatafile.readline(); temperature_database= temperature_database[0:-1] # 16
             salinity_database   = metadatafile.readline(); salinity_database   = salinity_database[   0:-1] # 17
             sound_speed_profile_model= metadatafile.readline(); sound_speed_profile_model = sound_speed_profile_model[0:-1] # 18
             propagation_model        = metadatafile.readline(); propagation_model         = propagation_model[        0:-1] # 19
             numeric_data_calibration = metadatafile.readline(); numeric_data_calibration  = numeric_data_calibration[ 0:-1] # 20
             metadatafile.close()
#            Convert the list of strings to a list of floats:
             source_levels = [float(xi) for xi in ssource_levels]
#            Load numerical data:
             matlab_data = loadmat(mfile,squeeze_me=True)
             total_number_of_grid_points = matlab_data['total_number_of_grid_points'] # 1
             c = total_number_of_grid_points.size
             if ( c == 0 ):
                total_number_of_grid_points = nan
             longitude = matlab_data['longitude'] # 2
             latitude  = matlab_data['latitude' ] # 3
             depth     = matlab_data['depth'    ] # 4
             frequency_band_definition = matlab_data['frequency_band_definition'] # 5
             frequency_count           = matlab_data['frequency_count'          ] # 6
             frequency                 = matlab_data['frequency'                ] # 7
             time                      = matlab_data['time'                     ] # 8
             spl_values                = matlab_data['spl_values'               ] # 9
             percentile_list = matlab_data['percentile_list'] # 10
             percentile_count = len( percentile_list )
             cA         = spl_values[0,:].size 
             time_count = spl_values[:,0].size
             percentile_values = zeros((cA,percentile_count))
#            Calculate the percentiles:
             for i in range(percentile_count):
                 percentile_values[:,i] = percentile(spl_values,percentile_list[i],axis=0)
#======================================================================
#         Make a dictionary of data: 
          data = {"format_version":format_version, "author":author, "institution":institution,"country_code":country_code,
          "contact":contact,"start_date":start_date,"end_date":end_date,"date_of_creation":date_of_creation,
          "purpose":purpose,"data_uuid":data_uuid,"data_type":data_type,"comments":comments,"expsetup":expsetup,
          "recorder_manufacturer":recorder_manufacturer,"recorder_serial_number":recorder_serial_number,
          "recorder_model":recorder_model,"builtin_hydrophone":builtin_hydrophone,
          "hydrophone_manufacturer":hydrophone_manufacturer,"hydrophone_sensitivity":hydrophone_sensitivity,
          "hydrophone_serial_number":hydrophone_serial_number,"hydrophone_model":hydrophone_model,  
          "calibration_frequency_count":calibration_frequency_count,"calibration_datetime":calibration_datetime,
          "calibration_factor":calibration_factor,"calibration_procedure":calibration_procedure,
          "reference_frequencies":reference_frequencies,"ais_database":ais_database,
          "source_levels":source_levels,
          "bathymetry_database":bathymetry_database,"temperature_database":temperature_database,
          "salinity_database":salinity_database,
          "sound_speed_profile_model":sound_speed_profile_model,"propagation_model":propagation_model,
          "numeric_data_calibration":numeric_data_calibration,
          "hydrophone_count":hydrophone_count,
          "total_number_of_grid_points":total_number_of_grid_points,
          "longitude":longitude,"latitude":latitude,"depth":depth,
          "frequency_count":frequency_count,"frequency_band_definition":frequency_band_definition,
          "frequency":frequency,
          "time_duty_on":time_duty_on,"time_duty_off":time_duty_off,"time_count":time_count,
          "time":time,"averaging_time":averaging_time,
          "spl_values":spl_values,
          "percentile_list":percentile_list,"percentile_count":percentile_count,"percentile_values":percentile_values}
#         Write the h5:
          write_edf(hfile,data)
          messagebox.showinfo("Done.", 'EDF file written.')     
    return
#======================================================================
# Function to end the GUI:
def byebye():
    messagebox.showinfo("Bye bye...", 'Hasta la vista baby.')
    root.destroy()
    return
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#======================================================================
#======================================================================
#                  Ladies and Gentlemen, the GUI:
#======================================================================
#======================================================================
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
root = Tk()
root.title("PAM2Py version 2.1")
# Styles:
fc = ttk.Style()
fc.configure('FC.TFrame', background='darkgreen')
bd = ttk.Style()
bd.configure('BD.TButton', font=('Helvetica', 18, 'bold'), width=20, background='white', foreground='black')
bq = ttk.Style()
bq.configure('BQ.TButton', font=('Helvetica', 18, 'bold'), width=20, background='white', foreground='black')    
cb = ttk.Style()
cb.configure('CB.TButton', font=('Helvetica', 16, 'bold'), width=20, background='yellow', foreground='black')
cb2 = ttk.Style()
cb2.configure('CB2.TCheckbutton',font=('Helvetica', 16, 'bold'))
ge = ttk.Style()
ge.configure('GE.TButton', font=('Helvetica', 16, 'bold'), width=30)
rb = ttk.Style()
rb.configure('RB.TButton', font=('Helvetica', 16, 'bold'), width=30, background='darkblue', foreground='white')
re = ttk.Style()
re.configure('RE.TRadiobutton',font=('Helvetica', 16, 'bold'), width=20, background='darkblue', foreground='white')
re2 = ttk.Style()
re2.configure('RE2.TRadiobutton',font=('Helvetica', 16, 'bold'), width=20)
te = ttk.Style()
te.configure('TE.TLabel', font=('Helvetica', 18, 'bold'), width=20, background='darkblue', foreground='white', anchor='center')
# Main GUI:
mainframe = ttk.Frame(root, padding="3 3 12 12", borderwidth=10, relief=RIDGE, style='FC.TFrame')
mainframe.grid(column=0, row=0)
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(   0, weight=1)
# Some integers:
jan  = IntVar(); jan.set(0)
jge  = IntVar(); jge.set(0)
jgn  = IntVar(); jgn.set(0)
jmd  = IntVar(); jmd.set(0)
jwo  = IntVar(); jwo.set(0)
jcal = IntVar(); jcal.set(0)
jges = IntVar(); jges.set(0)
jgea = IntVar(); jgea.set(0)
jmde = IntVar(); jges.set(0)
jmdn = IntVar(); jgea.set(0)
# Variables (YUP, all strings...):
matfile = StringVar(); matfile.set('Nothing selected...')
metfile = StringVar(); metfile.set('Nothing selected...')
sndfile = StringVar(); sndfile.set('Nothing selected...')
sndtype = StringVar(); sndtype.set('...')
CSVOUT  = StringVar(); CSVOUT.set('No')
EDFOUT  = StringVar(); EDFOUT.set('No')
gui2open = StringVar(); gui2open.set('Nothing selected...')
# Analysis/Calibration/Metadata Variables:
AIS_DB         = StringVar(); AIS_DB.set('AIS')
Atype          = StringVar(); Atype.set('PSD')
Author         = StringVar(); Author.set('Input your name')
AVtime         = StringVar(); AVtime.set('0.0')
Bathy_DB       = StringVar(); Bathy_DB.set('GEBCO')
Builtin        = StringVar(); Builtin.set('Unknown')
CalibCount     = StringVar(); CalibCount.set('0')
CalibD         = StringVar(); CalibD.set('20210000')
CalibF         = StringVar(); CalibF.set('0.0')
CalibP         = StringVar(); CalibP.set('Unknown')
Comments       = StringVar(); Comments.set('...')
Contact        = StringVar(); Contact.set('info@siplab.fct.ualg.pt')
Country_Code   = StringVar(); Country_Code.set('PT')
Creation_Date  = StringVar(); Creation_Date.set('20210000')
Ctype          = StringVar(); Ctype.set('None')
Data_Calibration= StringVar(); Data_Calibration.set('xxx-xxx-xxx-xxx')
Data_Type      = StringVar()
Data_Uuid      = StringVar(); Data_Uuid.set('xxx-xxx-xxx-xxx')
Depth          = StringVar(); Depth.set('0.0')
End_Date       = StringVar(); End_Date.set('20210000')
Envi           = StringVar(); Envi.set('Air')
Expsetup       = StringVar(); Expsetup.set('Input info')
FreqBand       = StringVar(); FreqBand.set('Unknown')
FreqCount      = StringVar(); FreqCount.set('0.0')
Format_Version = StringVar(); Format_Version.set('EDF1.0')
GG             = StringVar(); GG.set('0')
Hcut           = StringVar(); Hcut.set(' ')
HydroCount     = StringVar(); HydroCount.set('0')
HydroMa        = StringVar(); HydroMa.set('Unknown')
HydroMo        = StringVar(); HydroMo.set('Unknown')
HydroS         = StringVar(); HydroS.set('0')
HydroSN        = StringVar(); HydroSN.set('12345')
Institution    = StringVar(); Institution.set('University of Algarve')
Latitude       = StringVar(); Latitude.set('0.0')
Lcut           = StringVar(); Lcut.set('1')
Linlog         = StringVar(); Linlog.set('Logarithmic')
Longitude      = StringVar(); Longitude.set('0.0')
MH             = StringVar(); MH.set('-36')
PercCount      = StringVar(); PercCount.set('0')
PercList       = StringVar(); PercList.set('0.0')
Plottype       = StringVar(); Plottype.set('Both')
Propagation_Model= StringVar(); Propagation_Model.set('Ray model, Normal Mode model...')
Purpose        = StringVar(); Purpose.set('Unknown')
RecorderMa     = StringVar(); RecorderMa.set('Unknown')
RecorderSN     = StringVar(); RecorderSN.set('12345')
RecorderMo     = StringVar(); RecorderMo.set('Unknown')
RefFreq        = StringVar(); RefFreq.set('0.0')
Salinity_DB    = StringVar(); Salinity_DB.set('COPERNICUS')
SI             = StringVar(); SI.set('0')
Source_Levels  = StringVar(); Source_Levels.set('0.0')
SSP_Model      = StringVar(); SSP_Model.set('MacKenzie, Medwin, ...')
Start_Date     = StringVar(); Start_Date.set('20210000')
Temperature_DB = StringVar(); Temperature_DB.set('COPERNICUS')
TimeDO         = StringVar(); TimeDO.set('Unknown')
TimeDF         = StringVar(); TimeDF.set('Unknown')
VADC           = StringVar(); VADC.set('1.4142')
Welch          = StringVar(); Welch.set('0')
Winname        = StringVar(); Winname.set('Hann')
Wlength        = StringVar(); Wlength.set('1')
Wover          = StringVar(); Wover.set('50')
# A canvas to place the logo:
canvas = Canvas(mainframe, width =200, height=200, borderwidth=5, background='white')
thelogo = PhotoImage(file="jonas_logo.png")
canvas.create_image(110,120,image=thelogo)
ttk.Label(mainframe, text='Select Option:', style='TE.TLabel')
ttk.Radiobutton(mainframe, text="Experimental Data", style='RE.TRadiobutton', variable=gui2open, value='GED')
ttk.Radiobutton(mainframe, text="Numerical Data", style='RE.TRadiobutton', variable=gui2open, value='GND')
ttk.Radiobutton(mainframe, text="Write MetaData", style='RE.TRadiobutton', variable=gui2open, value='GMD')
BNX = ttk.Button(mainframe, text="Next", style='BD.TButton', command=whichgui) 
BQ  = ttk.Button(mainframe, text="Quit", style='BQ.TButton', command=byebye)
for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)
root.mainloop()
#======================================================================
# File cleaning:
if os.path.exists('Aft.mat'):
   os.remove('Aft.mat')
if os.path.exists('all.wav'):
   os.remove('all.wav')
if os.path.exists('all.flac'):
   os.remove('all.flac')
#======================================================================
#======================================================================
