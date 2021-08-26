# Tara - User Guide
User guide to access the data 
## Installation
It is recommended to install [anaconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html#regular-installation).

```bash
conda create --name tara python=3.8
conda activate tara
conda install -c conda-forge numpy scipy netcdf4 matplotlib boto3 git

git clone https://github.com/jcousineau/slf-py.git
git clone https://github.com/meracan/netcdf.git
git clone https://github.com/meracan/s3-netcdf.git
pip install -e ./slf-py
pip install -e ./netcdf
pip install -e ./s3-netcdf
```
(Developers) For running Telemac and post-processing:
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
aws_secret_access_key=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`
region=us-east-1
```
Please contact the administrator to get the `aws_access_key_id` and `aws_secret_access_key`.
## Models
There are 5 models:
- ERA5
-  rcp85.CanESM2.CanRCM4
- rcp85.CanESM2.CRCM5-UQAM
- rcp85.GFDL-ESM2M.WRF
- rcp85.MPI-ESM-MR.CRCM5-UQAM

To access a model:
```python
from s3netcdf import S3NetCDF
parameters={
	"name":"ERA5",     # name of model
	"bucket":"cccris", # name of s3 bucket
	"s3prefix":"data", # name of model
	"cacheLocation":"{PATH_TO_DIRECTORY}" #Path to directory where the data will be temporary stored
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
era5=S3NetCDF(parameters)

# Extract Mean Sea Level Pressure
frame0=era5['s','mslp',0]       # Get frame=0
frame0_10=era5['s','mslp',0:10] # Get frame 0 to 9

# Extract Mean Sea Level Pressure at specific date(s)
# Single date
userhourly = np.datetime64('1979-01-01T00:00:00')
index      = np.argsort(np.abs(hourly- userhourly))[0] # closest index
frame      = era5['s','mslp',index] 
# Multiple dates
userhourly = np.datetime64('1979-01-01T00:00:00') + np.arange(0,10)*np.timedelta64(1,'h')
indices    = np.argsort(np.abs(hourly- userhourly[:,np.newaxis]))[:,0] # closest indices
frames     = era5['s','mslp',indices]

# Extract Mean Sea Level Pressure to a Selafin File
from s3netcdf import nca2slf
nca2slf('mslp.slf',variables=['mslp'],startDate='1979-01-01T00:00:00',endDate='1979-01-01T10:00:00')
nca2slf('mslp.slf',variables=['mslp'],startDate='1979-01-01T00:00:00',endDate='1979-01-01T10:00:00',step=2,stepUnit="h") # With a 2 hr time step

# Extract Aggregated Daily Mean Sea Level Pressure
frame        = era5['ds','mslp',0]
frame_min    = frame[0]
frame_median = frame[1]
frame_mean   = frame[2]
frame_std    = frame[3]
frame_max    = frame[4]
frame        = era5['ds','mslp',0,2] # Mean Only

# Extract Daily Aggregated  Mean Sea Level Pressure to Selafin
# Note: this creates 5 variables in the Selafin object (MSLP_MIN,MSLP_MEDIAN,MSLP_MEAN,MSLP_STD,MSLP_MAX)
nca2slf('mslp.slf',group="ds",variables=['mslp'],startDate='1979-01-01T00:00:00',endDate='1979-01-10T00:00:00')
# Extract Aggregated  Mean Sea Level Pressure to Selafin
nca2slf('mslp.slf',group="as",variables=['mslp'])

 
```
