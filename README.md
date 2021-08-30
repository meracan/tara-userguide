# Tara - User Guide
User guide to access the data 
## Installation
It is recommended to install [anaconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html#regular-installation).

```bash
conda create --name tara python=3.8
conda activate tara
conda install -c conda-forge numpy scipy netcdf4 matplotlib boto3 git tqdm

git clone https://github.com/Julien-Cousineau/slf-py.git
git clone https://github.com/meracan/netcdf
git clone https://github.com/meracan/s3-netcdf
pip install -e ./slf-py
pip install -e ./netcdf
pip install -e ./s3-netcdf
```
(Developers-NOT TESTED) For running Telemac and post-processing:
```bash
git clone https://github.com/meracan/aws-tools.git
git clone https://github.com/meracan/aws-batch-api.git
git clone https://github.com/meracan/aws-telemac.git
pip install -e ./aws-tools
pip install -e ./aws-batch-api
pip install -e ./aws-telemac
```
## Credentials
Credentials is required to access AWS services. Credentials are not stored in python scripts but stored in a `credentials` file. The `credentials` file is located at `~/.aws/credentials` on Linux or macOS, or at ``C:\Users\`USERNAME`\.aws\credentials`` on Windows. This file can contain the credential details for the `default` profile and any named profiles. 
For more information: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html
For example, the file should look similar to the following.

**`~/.aws/credentials`**
```
[default]
aws_access_key_id=AKIAIOSFODNN7EXAMPLE
aws_secret_access_key=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
region=us-east-1
```
Please contact the administrator to get the `aws_access_key_id` and `aws_secret_access_key`.
## Models
There are 5 models:
- ERA5
- rcp85.CanESM2.CanRCM4
- rcp85.CanESM2.CRCM5-UQAM
- rcp85.GFDL-ESM2M.WRF
- rcp85.MPI-ESM-MR.CRCM5-UQAM

To access a model:
```python
from s3netcdf import S3NetCDF
parameters={
	"name":"ERA5",     # (required) name of model
	"bucket":"cccris", # (required,fixed) name of s3 bucket
	"s3prefix":"data", # (required,fixed) name of prefix for s3 bucket
	"cacheLocation":"{PATH_TO_DIRECTORY}" # Path to directory where the data will be temporary stored
}
era5=S3NetCDF(parameters)
```
## Data, Variables and Groups
Model contains 11 variables:
- `mslp` : Mean sea level pressure
- `u10` : U Velocity
- `v10` : V Velocity
- `uv10` : UV Velocity
- `dir10` : UV Direction
- `surge` : Surge
- `hs` : Significant Wave Height
- `tps` : Peak Period
- `tmm10` : Mean Period
- `dir` : Mean Direction
- `dspr` : Wave Spread

The access the data efficiently, each variable was stored under 9 groups depending on the request. The groups are :

- `s`: data is stored by frame (original Telemac results are saved here) 
- `t`: data is stored by timesries (Telemac results are transposed)
- `ds`: daily data by frame (data was post-process to calculate the daily  `min`,`median`,`mean`,`std` and `max)`
- `dt`: daily data by timeseries (data was post-process to calculate the daily  `min`,`median`,`mean`,`std` and `max)`
- `ys`: yearly data by frame (`min`,`median`,`mean`,`std` and `max)`
- `yt`: yearly data by timeseries (`min`,`median`,`mean`,`std` and `max)`
- `Ds`: Decade data by frame (`min`,`median`,`mean`,`std` and `max)`
- `Dt`: Decade data by timeseries (`min`,`median`,`mean`,`std` and `max)`
- `as`: Aggregated spatial data (`min`,`median`,`mean`,`std` and `max)`

## Mesh and Temporal Data
The are `352464` mesh nodes and time step is `1hr` for all models. To access the mesh coordinates and elements, and time arrays:
```python
era5   = S3NetCDF(parameters)
lng    = era5['node','x']
lat    = era5['node','y']
elem   = era5['elem','elem']
hourly = era5['time','time'] # hourly step

# To access the daily, yearly, decadal steps
daily   = era5['dtime','dtime']
yearly  = era5['ytime','ytime']
decadal = era5['Dtime','Dtime']
```
## Examples - Frames
```python
import numpy as np

era5=S3NetCDF(parameters)

lng    = era5['node','x']
lat    = era5['node','y']
elem   = era5['elem','elem']
hourly = era5['time','time']    # hourly step
daily   = era5['dtime','dtime'] # daily step
yearly  = era5['ytime','ytime'] # yearly step
decadal = era5['Dtime','Dtime'] # decadal step

# Extract variable at frame(s)
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

# Extract variable to a Selafin File
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
```
### Plot Frame using Matplotlib
```python
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

```

### Plot Timeseries
```python

era5=S3NetCDF(parameters)
lng   = era5['node','x']
lat   = era5['node','y']
vname ="surge"


# Extract variable at node0
ts      = era5['t',vname,0]

# Extract variable at specific tide stations
tideStations = [
  dict(xy=[-123.279, 49.297],id=7735,name="Vancouver"),
  dict(xy= [-130.560, 54.299],id=9354,name="Prince Rupert"),
  dict(xy=[-125.122, 48.871],id=8545,name="Bamfield"),
]

def getClosestIndices(x,y,stations):
	from scipy import spatial
	xy   = np.column_stack((x,y))
	tree = spatial.KDTree(xy)
  
	pts  = np.asarray(list(map(lambda x:x['xy'],stations)))
	return tree.query(pts)[1]

indices = getClosestIndices(lng,lat,tideStations)
ts      = era5['t',vname,indices]

```


### Simulation
DEMO
```python
from awstelemac import AWSTelemac
from awstools import Batch

# Create simulation
modelId="ERA5"
era5=AWSTelemac(modelId=modelId)
casId=era5.uploadFromCas(casPath,module="telemac2d",keywords={"TIME STEP":30})

# Run simulation
batch=Batch() # AWS api
batch.send(modelId=modelId,casId=casId)
```

