import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from read_mesonet_data import get_nysm_data, mtime, TEMP_2M, PRESSURE, AVG_WIND_SPEED, MAX_WIND_SPEED, WIND_DIRECTION, prcp_evol
#exec(open('read_mesonet_data.py').read())

def find_coords(lon,lat,klat,klon):
   dl = 0.02
   minlat = klat - dl
   maxlat = klat + dl
   minlon = klon - dl
   maxlon = klon + dl
   wh = np.where((lon < maxlon) & (lon > minlon) & (lat > minlat) & (lat < maxlat))
   domi = np.int(np.mean(wh[0]))
   domj = np.int(np.mean(wh[1]))
   return domi,domj

def remove_axis_spines(ax):
    locs = ['top','left','right']
    for i in locs:
        ax.spines[i].set_visible(False)

def make_meteogram(station):
    mesolat, mesolon, mname, loc = get_nysm_data(station)
    kwargs = {'alpha':0.5}

    plt.figure(figsize=(10,7))

    ax1 = plt.subplot(411)
    ax1.grid(axis='y',linewidth=0.5)
    ax1.plot(mtime, TEMP_2M[loc,:],color='lightblue')
    ax1.fill_between(mtime,TEMP_2M[loc,:],np.min(TEMP_2M[loc,:])-5,color='lightblue',**kwargs)
    ax1.set_title('2-m Temperature (deg C)')
    plt.xlim(datetime(2017,10,29,0),datetime(2017,10,30,12))
    ax1.set_ylim(np.nanmin(TEMP_2M[loc,:])-1,np.nanmax(TEMP_2M[loc,:])+5)
    remove_axis_spines(ax1)

    pressure = PRESSURE[loc,:]
    mask = np.isfinite(pressure)

    ax2 = plt.subplot(412)
    ax2.grid(axis='y',linewidth=0.5)
    ax2.plot(mtime[mask], pressure[mask],color='brown')
    ax2.fill_between(mtime[mask], pressure[mask], 850, color='brown',**kwargs)
    ax2.set_title('Pressure (hPa)')
    plt.xlim(datetime(2017,10,29,0),datetime(2017,10,30,12))
    ax2.set_ylim(np.nanmin(PRESSURE[loc,:])-20,np.nanmax(PRESSURE[loc,:])+1)
    remove_axis_spines(ax2)

    ax3 = plt.subplot(413)
    ax3.grid(axis='y',linewidth=0.5)
    ax3.plot(mtime, AVG_WIND_SPEED[loc,:],color='darkblue')
    ax3.fill_between(mtime, AVG_WIND_SPEED[loc,:],0,color='darkblue',**kwargs)
    ax3.plot(mtime, MAX_WIND_SPEED[loc,:],color='lightblue',linestyle='--')
    ax3.fill_between(mtime, MAX_WIND_SPEED[loc,:],0,color='lightblue',**kwargs)
    remove_axis_spines(ax3)
    ax5 = ax3.twinx()
    ax5.grid(axis='y',c='k',linewidth=0.5)
    ax5.scatter(mtime[::5], WIND_DIRECTION[loc,::5],color='orange',marker='o',**kwargs)
    ax5.set_yticks(ticks=[0,90,180,270,360])
    ax5.set_yticklabels(['N','E','S','W','N'])
    ax5.set_title('10-m Wind Speed/Gust (m s$^{-1}$) and Direction')
    plt.xlim(datetime(2017,10,29,0),datetime(2017,10,30,12))
    remove_axis_spines(ax5)

    ax4 = plt.subplot(414)
    ax4.grid(axis='y',linewidth=0.5)
    ax4.plot(mtime, prcp_evol[loc,:],color='lightgreen')
    ax4.fill_between(mtime, prcp_evol[loc,:],0,color='lightgreen',**kwargs)
    ax4.set_title('Precipitation (mm)')
    plt.xlim(datetime(2017,10,29,0),datetime(2017,10,30,12))
    remove_axis_spines(ax4)
    
    ax4.text(1., 0.01, 'Plot by L. Gaudet',
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax4.transAxes,
        color='grey', fontsize=10)
    plt.suptitle(f'Meteogram for {mname}', fontweight='bold')
    plt.tight_layout(rect=[0,0.03,1,0.95])
    plt.savefig(f'./nysm_meteogram_{station}.png', type='png',dpi=300)
    plt.show()

station_choice = 'VOOR' #specify the station identifier that you want to see a meteogram of
make_meteogram(station_choice)



