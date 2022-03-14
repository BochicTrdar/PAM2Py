#==========================================================================
#               Writing a .h5 file created according to the
#                    JONAS Exchange Data Format Proposal
#==========================================================================
# Python version 
# Adapted from write_edf.m
# Written by Orlando Camargo Rodriguez
# Faro, Sex 29 Jan 2021 17:54:13 WET 
# Unlike the *.m version this function defines all fields
#==========================================================================
#
# The complete field description can be found at the JONAS Deliverable D4.3 
#
# write_edf(filename,data)
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
# I believe strings can be encoded only in the attributes...
#==========================================================================
def write_edf(filename=None,data=None):
    h5 = h5py.File(filename, 'w')
    ambient_noise_dataset = h5.create_group('ambient_noise_dataset')
    analysis_metadata     = h5.create_group('analysis_metadata'    )
#--------------------------------------------------------------------------
    frequencyg                  = ambient_noise_dataset.create_group('frequency')
    position                    = ambient_noise_dataset.create_group('position')
    sound_pressure_levels       = ambient_noise_dataset.create_group('sound_pressure_levels')
    sound_pressure_levels_stats = ambient_noise_dataset.create_group('sound_pressure_levels_stats')
    time                        = ambient_noise_dataset.create_group('time')
#--------------------------------------------------------------------------
    experimental    = analysis_metadata.create_group('experimental'   )
    numerical_model = analysis_metadata.create_group('numerical_model')
#--------------------------------------------------------------------------
    frequencyg['frequency_band_definition'] = data['frequency_band_definition']
    frequencyg['frequency'                ] = data['frequency']
    frequencyg['frequency_count'          ] = data['frequency_count']  
#--------------------------------------------------------------------------
    position['depth'           ] = data['depth']
    position['hydrophone_count'] = data['hydrophone_count'] 
    position['latitude'        ] = data['latitude'        ]
    position['longitude'       ] = data['longitude'       ]
    position['total_number_of_grid_points'] = data['total_number_of_grid_points']
#--------------------------------------------------------------------------
    sound_pressure_levels['spl_values'] = data['spl_values']
#--------------------------------------------------------------------------
    sound_pressure_levels_stats['percentile_count' ] = data['percentile_count' ]
    sound_pressure_levels_stats['percentile_list'  ] = data['percentile_list'  ]
    sound_pressure_levels_stats['percentile_values'] = data['percentile_values']
#--------------------------------------------------------------------------
    time['time'      ] = data['time']
    time['time_count'] = data['time_count']
#--------------------------------------------------------------------------
    calibration = experimental.create_group('calibration')
    hydrophone  = experimental.create_group('hydrophone' )
    recorder    = experimental.create_group('recorder'   )
#--------------------------------------------------------------------------
    calibration['calibration_procedure'      ] = data['calibration_procedure'      ]
    calibration['calibration_datetime'       ] = data['calibration_datetime'       ]
    calibration['calibration_factor'         ] = data['calibration_factor'         ]
    calibration['calibration_frequency_count'] = data['calibration_frequency_count']
    calibration['reference_frequencies'      ] = data['reference_frequencies'      ]
#--------------------------------------------------------------------------
    numerical_model['source_levels'] = data['source_levels']
#--------------------------------------------------------------------------
# Attributes:
#--------------------------------------------------------------------------
    h5.attrs['author'          ] = data['author'          ].encode()
    h5.attrs['comments'        ] = data['comments'        ].encode()
    h5.attrs['contact'         ] = data['contact'         ].encode()
    h5.attrs['country_code'    ] = data['country_code'    ].encode()
    h5.attrs['data_type'       ] = data['data_type'       ].encode()
    h5.attrs['data_uuid'       ] = data['data_uuid'       ].encode()
    h5.attrs['format_version'  ] = data['format_version'  ].encode()
    h5.attrs['institution'     ] = data['institution'     ].encode()
    h5.attrs['purpose'         ] = data['purpose'         ].encode()
    h5.attrs['date_of_creation'] = data['date_of_creation']
    h5.attrs['end_date'        ] = data['end_date'        ]
    h5.attrs['start_date'      ] = data['start_date'      ]
#--------------------------------------------------------------------------
    experimental.attrs['expsetup'] = data['expsetup'].encode()
#--------------------------------------------------------------------------
    recorder.attrs['recorder_manufacturer' ] = data['recorder_manufacturer' ].encode()
    recorder.attrs['recorder_serial_number'] = data['recorder_serial_number'].encode()
    recorder.attrs['recorder_model'        ] = data['recorder_model'        ].encode()
    recorder.attrs['builtin_hydrophone'    ] = data['builtin_hydrophone'    ].encode()
#--------------------------------------------------------------------------
    hydrophone.attrs['hydrophone_manufacturer' ] = data['hydrophone_manufacturer' ].encode()
    hydrophone.attrs['hydrophone_serial_number'] = data['hydrophone_serial_number'].encode()
    hydrophone.attrs['hydrophone_model'        ] = data['hydrophone_model'        ].encode()
    hydrophone.attrs['hydrophone_sensitivity'  ] = data['hydrophone_sensitivity'  ]
#--------------------------------------------------------------------------
    numerical_model.attrs['sound_speed_profile_model'] = data['sound_speed_profile_model'].encode()
    numerical_model.attrs['propagation_model'        ] = data[        'propagation_model'].encode()
    numerical_model.attrs['numeric_data_calibration' ] = data[ 'numeric_data_calibration']
    numerical_model.attrs['ais_database'        ] = data[        'ais_database'].encode()
    numerical_model.attrs['bathymetry_database' ] = data[ 'bathymetry_database'].encode()
    numerical_model.attrs['temperature_database'] = data['temperature_database'].encode()
    numerical_model.attrs['salinity_database'   ] = data[   'salinity_database'].encode()
#--------------------------------------------------------------------------
    time.attrs['time_duty_on' ] = data['time_duty_on' ].encode()
    time.attrs['time_duty_off'] = data['time_duty_off'].encode()
#--------------------------------------------------------------------------
    sound_pressure_levels.attrs['averaging_time'] = data['averaging_time']
#--------------------------------------------------------------------------
    h5.close()
    return
