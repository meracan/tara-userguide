import numpy as np
from s3netcdf import S3NetCDF
import matplotlib.pyplot as plt
from scipy import spatial

parameters={
	"name":"ERA5",     # name of model
# 	"name":"rcp85.CanESM2.CanRCM4",     # name of model
	"bucket":"cccris", # name of s3 bucket
	"s3prefix":"data", # name of model
	"cacheLocation":"output", # Path to directory where the data will be temporary stored
	
	"autoRemove":False, # Keep s3 files once stored into memory
	"credentials":{"profile_name":"tara"},
}

tideStations = [
  dict(xy=[-123.279, 49.297],id=7735,name="Vancouver"),
  dict(xy= [-130.560, 54.299],id=9354,name="Prince Rupert"),
  dict(xy=[-125.122, 48.871],id=8545,name="Bamfield"),
]

waveStations = [
  dict(xy=[-132.42,54.38],id='c46145',name="Central Dixon Entrance"), 
  dict(xy= [-123.73, 49.34],id='c46146',name="Halibut Bank"),
  dict(xy=[-131.14 , 53.57],id='c46183',name="North Hecate Strait"), 
  dict(xy=[-126, 48.83],id='c46206',name="La Perouse Bank")
]

def getClosestIndices(x,y,stations):
  xy   = np.column_stack((x,y))
  tree = spatial.KDTree(xy)
  
  pts  = np.asarray(list(map(lambda x:x['xy'],stations)))
  return tree.query(pts)[1]


def run():
  
  era5=S3NetCDF(parameters)
  
  lng    = era5['node','x']
  lat    = era5['node','y']
  elem   = era5['elem','elem']
  indices = getClosestIndices(lng,lat,tideStations)
  hourly = era5['time','time'] # hourly step
  daily   = era5['dtime','dtime']
  # yearly  = era5['ytime','ytime']
  # decadal = era5['Dtime','Dtime']
  
  vname ="surge"
  ts      = era5['t',vname,indices]
  plt.plot(hourly, ts[0])
  plt.savefig("output/ts.{}.png".format(vname), bbox_inches='tight')
  
  # # Wave
  # indices = getClosestIndices(lng,lat,tideStations)
  # ts      = era5['t','mslp',indices]
  # plt.plot(hourly, ts[0])
  # plt.savefig("output/timeseries.png", bbox_inches='tight')  
  
  

if __name__ == "__main__":
  run()
