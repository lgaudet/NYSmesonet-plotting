import numpy as np
import glob
import pandas as pd
from datetime import datetime

indir = '/glade/work/lgaudet/research/data/'

timeFormat = '%Y-%m-%d %H:%M:%S UTC'
parseTime = lambda x: datetime.strptime(x, timeFormat)

df = pd.concat([pd.read_csv(f,parse_dates=['time'],date_parser=parseTime) for f in sorted(glob.glob(indir+'2017*.csv'))])
df.set_index(['station','time'], inplace = True)
mtime = pd.to_datetime(df.index.levels[1].values)
STN = df.index.levels[0].values.tolist()

nstn = len(STN)
ntime = len(mtime)
RH = np.zeros((nstn,ntime))
PRECIP_INC = np.zeros((nstn,ntime))
PRECIP_LOC = np.zeros((nstn,ntime))
PRECIP_MAX_INT = np.zeros((nstn,ntime))
TEMP_2M = np.zeros((nstn,ntime))
TEMP_9M = np.zeros((nstn,ntime))
PRESSURE = np.zeros((nstn,ntime))
WIND_DIRECTION = np.zeros((nstn,ntime))
MAX_WIND_SPEED = np.zeros((nstn,ntime))
AVG_WIND_SPEED = np.zeros((nstn,ntime))
for ii, stn in enumerate(STN):
    RH[ii,:] = df.loc[stn,'relative_humidity [percent]'].values
    PRECIP_INC[ii,:] = df.loc[stn,'precip_incremental [mm]'].values
    PRECIP_LOC[ii,:] = df.loc[stn,'precip_local [mm]'].values
    PRECIP_MAX_INT[ii,:] = df.loc[stn,'precip_max_intensity [mm/min]'].values
    TEMP_2M[ii,:] = df.loc[stn,'temp_2m [degC]'].values
    TEMP_9M[ii,:] = df.loc[stn,'temp_9m [degC]'].values
    PRESSURE[ii,:] = df.loc[stn,'station_pressure [mbar]'].values
    WIND_DIRECTION[ii,:] = df.loc[stn,'wind_direction_prop [degrees]'].values
    MAX_WIND_SPEED[ii,:] = df.loc[stn,'max_wind_speed_prop [m/s]'].values
    AVG_WIND_SPEED[ii,:] = df.loc[stn,'avg_wind_speed_prop [m/s]'].values

prcp_evol = np.zeros((nstn,ntime))
prcp_save = 0.
for tt in range(0,ntime):
    prcp_evol[:,tt] = prcp_save + PRECIP_INC[:,tt]
    prcp_save = prcp_evol[:,tt]

df = pd.read_csv(indir+'nysm.csv',index_col=0)
mstn = df.index.values.tolist()
mlat = df['lat [degrees]'].values
mlon = df['lon [degrees]'].values

def resample(var,times1,varname):
   df = pd.DataFrame(times1,columns=['date'])
   df['%s'%(varname)] = var
   df['datetime'] = pd.to_datetime(df['date'])
   df = df.set_index('datetime')
   df.drop(['date'],axis=1,inplace=True)
   #var_1hr = df
   df['%s'%(varname)] = df['%s'%(varname)].apply(pd.to_numeric, errors='coerce')
   var_1hr = df.resample('1H').sum()
   return var_1hr

def resample_hrly(var,times1,varname):
   df = pd.DataFrame(times1,columns=['date'])
   df['%s'%(varname)] = var
   df['datetime'] = pd.to_datetime(df['date'])
   df = df.set_index('datetime')
   df.drop(['date'],axis=1,inplace=True)
   #var_1hr = df
   df['%s'%(varname)] = df['%s'%(varname)].apply(pd.to_numeric, errors='coerce')
   var_1hr = df.resample('1H').mean()
   return var_1hr

def get_nysm_data(station):
    indir = '/glade/work/lgaudet/research/data/'
    df = pd.read_csv(indir+'nysm.csv',index_col=0)
    mstn = df.index.values.tolist()
    mlat = df['lat [degrees]'].values
    mlon = df['lon [degrees]'].values
    name = df['name'].values

    mloc = mstn.index(station)
    mesolat, mesolon = mlat[mloc], mlon[mloc]
    mname = name[mloc]
    loc = STN.index(station)
    return mesolat, mesolon, mname, loc

