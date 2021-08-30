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


def plotSingleFrame():
  import matplotlib.pyplot as plt
  import matplotlib.colors as colors
  import matplotlib.tri as tri
  
  era5=S3NetCDF(parameters)
  vname   = 'mslp'
  frame = np.squeeze(era5['s',vname,0]) 
  x     = era5['node','x']
  y     = era5['node','y']
  elem  = era5['elem','elem']
  Tri   = tri.Triangulation(x, y,elem)
  
  fig1, ax1 = plt.subplots()
  levels = np.arange(95, 105, 0.5)
  gamma = 1.3  
  
  tcf = ax1.tricontourf(Tri,frame,levels=levels, cmap="jet", norm=colors.PowerNorm(gamma=gamma))
  fig1.colorbar(tcf)
  ax1.tricontour(Tri, frame, colors='k')
  ax1.set_title('Contour plot')
  plt.savefig("output/tmp.png", bbox_inches='tight')


def plotMultipleFrames():
  import matplotlib.pyplot as plt
  import matplotlib.colors as colors
  from matplotlib.animation import FuncAnimation,PillowWriter
  import matplotlib.tri as tri
  
  vname   = 'mslp'
  era5    = S3NetCDF(parameters)
  frames  = era5['s',vname,:24] 
  nframes = frames.shape[0]
  x       = era5['node','x']
  y       = era5['node','y']
  elem    = era5['elem','elem']
  Tri     = tri.Triangulation(x, y,elem)
  
  fig1, ax1 = plt.subplots()
  levels = np.arange(95, 105, 0.5)
  gamma = 1.3
  
  isColorBar=False
  def update(i):
    print(i)
    nonlocal isColorBar
    frame=frames[i]
    tcf = ax1.tricontourf(Tri,frame,levels=levels, cmap="jet", norm=colors.PowerNorm(gamma=gamma))
    if not isColorBar:
      fig1.colorbar(tcf)
      isColorBar=True
    
    
  anim = FuncAnimation(fig1, update, frames=nframes)
  writer = PillowWriter(fps=4)  
  anim.save("output/ani.gif", writer=writer)
  

if __name__ == "__main__":
  plotSingleFrame()
  plotMultipleFrames()