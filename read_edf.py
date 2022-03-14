#==========================================================================
#               Reading the .h5 file created according to the
#                    JONAS Exchange Data Format Proposal
#==========================================================================
# Python version 
# Adapted from read_edf.m
# Written by Orlando Camargo Rodriguez
# Faro, Qua 03 Fev 2021 19:54:12 WET 
#==========================================================================
#
# The complete field description can be found at the JONAS Deliverable D4.3 
#
# DATA = read_edf('filename.h5')
#==========================================================================
# Don't like it? Don't use it...
#==========================================================================
from numpy import *
import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
import h5py
#==========================================================================
# Function description: reads a ".h5" file taking into account the parameters
# defined at the JONAS Exchange Data Format proposal.
#==========================================================================
#List of parameters:
#format_version 
#author 
#institution
#country_code
#contact
#start_date
#end_date
#date_of_creation
#purpose
#data_uuid
#data_type
#comments
#expsetup
#recorder_manufacturer
#recorder_serial_number
#recorder_model
#builtin_hydrophone
#hydrophone_manufacturer
#hydrophone_sensitivity
#hydrophone_serial_number
#hydrophone_model
#calibration_frequency_count
#calibration_datetime
#calibration_factor
#calibration_procedure
#reference_frequencies
#ais_database
#source_levels
#bathymetry_database
#emperature_database
#salinity_database
#sound_speed_profile_model
#propagation_model
#numeric_data_calibration
#hydrophone_count
#total_number_of_grid_points
#longitude
#latitude
#depth
#frequency_count
#frequency_band_definition
#frequency
#time_duty_on
#time_duty_off
#time_count
#time
#averaging_time
#spl_values
#percentile_list
#percentile_count
#percentile_values
#==========================================================================
# General strategy: read attributes and datasets, select common variables, 
# then read non-common variables case by case
#==========================================================================
# Let's go:
def read_edf(filename=None):
    data = []
#   frequency_band_definition = '1/3-octave band levels' # I believe this is not needed...
    h5 = h5py.File(filename, 'r')
    attributes = h5.attrs
    author         = attributes['author'        ].decode().strip()
    comments       = attributes['comments'      ].decode().strip()
    contact        = attributes['contact'       ].decode().strip()
    country_code   = attributes['country_code'  ].decode().strip()
    data_type      = attributes['data_type'     ].decode().strip()
    data_uuid      = attributes['data_uuid'     ].decode().strip()
    format_version = attributes['format_version'].decode().strip()
    institution    = attributes['institution'   ].decode().strip()
    purpose        = attributes['purpose'       ].decode().strip()
    date_of_creation = attributes['date_of_creation']
    end_date         = attributes[  'end_date'      ]
    start_date       = attributes['start_date'      ]
#-----------------------------------------------------------------------------
    ambient_noise_dataset = h5['ambient_noise_dataset'] # ['frequency', 'position', 'sound_pressure_levels', 'sound_pressure_levels_stats', 'time']
    analysis_metadata     = h5['analysis_metadata'    ]
    frequency_dataset     = ambient_noise_dataset['frequency']
    position_dataset      = ambient_noise_dataset['position' ]
    soundplv_dataset      = ambient_noise_dataset['sound_pressure_levels' ] # ['spl_values']
    soundplv_attrs        = ambient_noise_dataset['sound_pressure_levels' ].attrs # ['averaging_time']
    soundsts_dataset      = ambient_noise_dataset['sound_pressure_levels_stats'] # ['percentile_count', 'percentile_list', 'percentile_values']
    time_dataset          = ambient_noise_dataset['time'] # ['time', 'time_count']
    time_attrs            = ambient_noise_dataset['time'].attrs # ['time_duty_off', 'time_duty_on']
#==========================================================================
    expinfo  = analysis_metadata['experimental']
    expattrs = expinfo.attrs
#==========================================================================
    frequency                 = frequency_dataset['frequency'][:]
    frequency_band_definition = frequency_dataset['frequency_band_definition'][...]
    frequency_count           = frequency_dataset['frequency_count'][...]
#==========================================================================
    longitude = position_dataset['longitude'][:]
    latitude  = position_dataset['latitude' ][:]
    depth     = position_dataset['depth'    ][:]
#==========================================================================
    time        = time_dataset['time'      ][:]
    time_count  = time_dataset['time_count'][...]
#==========================================================================
    spl_values  = soundplv_dataset['spl_values'][:]
#==========================================================================
    percentile_count = soundsts_dataset['percentile_count' ][...]
    percentile_list  = soundsts_dataset['percentile_list'  ][:]
    percentile_values= soundsts_dataset['percentile_values'][:]
#==========================================================================
# Data Type cases:
#==========================================================================
# NOT DEFINED:
    if len(data_type) == 0:
       print('No data_type defined in the EDF file')
       expsetup = []
       recorder_manufacturer    = [] 
       recorder_serial_number   = []
       recorder_model           = []
       builtin_hydrophone       = []
       hydrophone_manufacturer  = []
       hydrophone_sensitivity   = []
       hydrophone_serial_number = []
       hydrophone_model         = []
       calibration_frequency_count = []
       calibration_datetime     = []
       calibration_factor       = []
       calibration_procedure    = []
       reference_frequencies    = []
       ais_database             = []
       source_levels            = []
       bathymetry_database      = []
       temperature_database     = []
       salinity_database        = []
       sound_speed_profile_model= []
       propagation_model        = []
       numeric_data_calibration = []
       hydrophone_count         = []
       total_number_of_grid_points = []
       time_duty_on  = time_attrs['time_duty_on' ].decode().strip()
       time_duty_off = time_attrs['time_duty_off'].decode().strip()
       averaging_time = soundplv_attrs['averaging_time'][:]
#==========================================================================
# EXPERIMENTAL:
    elif data_type == 'Experimental':
       print('Reading Experimental data_type...')
#======================================================================
       calibration          = expinfo['calibration'] # ['calibration_datetime', 'calibration_factor', 'calibration_frequency_count', 'calibration_procedure', 'reference_frequencies']
       calibration_procedure= calibration['calibration_procedure'][...]
       calibration_datetime = calibration['calibration_datetime'][...]
       calibration_factor   = calibration['calibration_factor'][...]
       calibration_frequency_count = calibration['calibration_frequency_count'][...]
       reference_frequencies= calibration['reference_frequencies'][...]
#======================================================================
       recorder = expinfo['recorder'].attrs # ['builtin_hydrophone', 'recorder_manufacturer', 'recorder_model', 'recorder_serial_number']
       recorder_manufacturer = recorder['recorder_manufacturer' ].decode().strip() 
       recorder_serial_number= recorder['recorder_serial_number'].decode().strip() 
       recorder_model        = recorder['recorder_model'        ].decode().strip()
       builtin_hydrophone    = recorder['builtin_hydrophone'    ].decode().strip()
#======================================================================
       hydrophone = expinfo['hydrophone'].attrs # ['hydrophone_manufacturer', 'hydrophone_model', 'hydrophone_sensitivity', 'hydrophone_serial_number']
       hydrophone_manufacturer = hydrophone['hydrophone_manufacturer' ].decode().strip()
       hydrophone_serial_number= hydrophone['hydrophone_serial_number'].decode().strip()
       hydrophone_model        = hydrophone['hydrophone_model'        ].decode().strip()
       hydrophone_sensitivity  = hydrophone['hydrophone_sensitivity'  ]
#======================================================================
       time_duty_on  = time_attrs['time_duty_on' ].decode().strip()
       time_duty_off = time_attrs['time_duty_off'].decode().strip()
#======================================================================
       averaging_time = soundplv_attrs['averaging_time']
#======================================================================
       hydrophone_count = position_dataset['hydrophone_count'][...]
#======================================================================
       expsetup = expattrs['expsetup'].decode().strip()
#======================================================================
       ais_database         = []
       source_levels        = []
       bathymetry_database  = []
       temperature_database = []
       salinity_database    = []
       sound_speed_profile_model   = []
       propagation_model           = []
       numeric_data_calibration    = []
       total_number_of_grid_points = []
#==========================================================================
# NUMERICAL:
    elif data_type == 'Numerical':
       print('Reading Numerical data_type...')
       numerical_model = analysis_metadata['numerical_model']
       numerical_attrs = numerical_model.attrs
       expsetup               = []
       recorder_manufacturer  = []
       recorder_serial_number = []
       recorder_model         = []
       builtin_hydrophone     = []
       hydrophone_manufacturer= []
       hydrophone_sensitivity = []
       hydrophone_serial_number=[]
       hydrophone_model       = []
       calibration_frequency_count = []
       calibration_datetime   = []
       calibration_factor     = []
       calibration_procedure  = []
       reference_frequencies  = []
       hydrophone_count       = []
       time_duty_on           = []
       time_duty_off          = []
       averaging_time         = []
       source_levels          = numerical_model['source_levels'       ]
       ais_database           = numerical_attrs['ais_database'        ].decode().strip()
       bathymetry_database    = numerical_attrs['bathymetry_database' ].decode().strip()
       temperature_database   = numerical_attrs['temperature_database'].decode().strip()
       salinity_database      = numerical_attrs['salinity_database'   ].decode().strip()
       sound_speed_profile_model = numerical_attrs['sound_speed_profile_model'].decode().strip()
       propagation_model         = numerical_attrs['propagation_model'        ].decode().strip()
       numeric_data_calibration    = numerical_attrs['numeric_data_calibration'    ]
       total_number_of_grid_points = position_dataset['total_number_of_grid_points']
#==========================================================================
# NO VALID:
    else:
       print('No valid data_type was defined in the EDF file.')
       print('It should be defined has Experimental or Numerical in the EDF metadata file')
       averaging_time         = []
       builtin_hydrophone     = []
       calibration_datetime   = []
       calibration_factor     = []
       calibration_procedure  = []
       expsetup               = []
       hydrophone_count       = []
       hydrophone_manufacturer= []
       hydrophone_model       = []
       hydrophone_sensitivity = []
       propagation_model      = []
       recorder_manufacturer  = []
       recorder_model         = []
       recorder_serial_number = []
       reference_frequencies  = []
       ais_database           = []
       source_levels          = []
       time_duty_on           = []
       time_duty_off          = []
       bathymetry_database    = []
       salinity_database      = []
       temperature_database   = []
       calibration_frequency_count= []
       hydrophone_serial_number   = []
       numeric_data_calibration   = []
       sound_speed_profile_model  = []
       total_number_of_grid_points= []
#==========================================================================
# Close the file:
    h5.close()
#==========================================================================
# Return data as a dictionary:
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
    return data
