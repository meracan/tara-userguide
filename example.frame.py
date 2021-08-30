import numpy as np
from s3netcdf import S3NetCDF

parameters={
	"name":"ERA5",     # name of model
# 	"name":"rcp85.CanESM2.CanRCM4",     # name of model
	"bucket":"cccris", # name of s3 bucket
	"s3prefix":"data", # name of model
	"cacheLocation":"output", # Path to directory where the data will be temporary stored
	
	"autoRemove":False, # Keep s3 files once stored into memory
	"credentials":{"profile_name":"tara"},
}

def run():
  
  era5=S3NetCDF(parameters)
  
  lng    = era5['node','x']
  lat    = era5['node','y']
  elem   = era5['elem','elem']
  hourly = era5['time','time']    # hourly step
  daily   = era5['dtime','dtime'] # daily step
  yearly  = era5['ytime','ytime'] # yearly step
  decadal = era5['Dtime','Dtime'] # decadal step
  
  # Extract variable
  vname='mslp'
  frame0=era5['s',vname,0]       # Get frame=0
  frame0_10=era5['s',vname,0:10] # Get frame 0 to 9
  
  # Extract Mean Sea Level Pressure at specific date(s)
  # Single date
  userhourly = np.datetime64('1979-01-01T00:00:00')
  index      = np.argsort(np.abs(hourly- userhourly))[0] # closest index
  frame      = era5['s',vname,index] 
  # Multiple dates
  userhourly = np.datetime64('1979-01-01T00:00:00') + np.arange(0,10)*np.timedelta64(1,'h')
  indices    = np.argsort(np.abs(hourly- userhourly[:,np.newaxis]))[:,0] # closest indices
  frames     = era5['s',vname,indices]
  
  #Extract variable to a Selafin File
  era5.toslf('output/{}.slf'.format(vname),variables=[vname],startDate='1979-01-01T00:00:00',endDate='1979-01-01T10:00:00')
  era5.toslf('output/{}.slf'.format(vname),variables=[vname],startDate='1979-01-01T00:00:00',endDate='1979-01-01T10:00:00',step=2,stepUnit="h") # With a 2 hr time step
  
  # Extract Aggregated Daily data
  frame        = era5['ds',vname,0]
  
  frame_min    = frame[0] # min
  frame_median = frame[1] # median
  frame_mean   = frame[2] # avg
  frame_std    = frame[3] # std
  frame_max    = frame[4] # max
  
  frame        = era5['ds',vname,0,2] # Get mean values only
  
  # Extract Daily Aggregated data to Selafin
  # Note: this creates 5 variables in the Selafin object (MSLP_MIN,MSLP_MEDIAN,MSLP_MEAN,MSLP_STD,MSLP_MAX)
  era5.toslf('output/{}.daily.slf'.format(vname),group="ds",variables=[vname],startDate='1979-01-01T00:00:00',endDate='1979-01-03T00:00:00')
  # Extract Aggregated data to Selafin
  era5.toslf('output/{}.agg.slf'.format(vname),group="as",variables=[vname])
  

if __name__ == "__main__":
  run()
