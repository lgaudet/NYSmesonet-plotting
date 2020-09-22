import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
import geoplot as gplt
import geoplot.crs as gcrs
from datetime import datetime
from affine import Affine
from rasterio import features
import xarray as xr
import cartopy.crs as ccrs
from matplotlib.colors import ListedColormap, BoundaryNorm
from read_mesonet_data import mlat, mlon, mstn, mtime, STN, prcp_evol

#the NYSmesonet station location data includes all 126 stations
#the NYSmesonet station meteorological data only includes 124 stations
#therefore, we have to make sure we are indexing the correct data
lats, lons, stns = [], [], []
for i in range(0,len(STN)):
   ii = mstn.index(STN[i]) #using the lat/lon index from metadata, find the corresponding index in actual data
   lats.append(mlat[ii])
   lons.append(mlon[ii])
   stns.append(STN[i])

nws_precip_colors = ["#ffffff","#04e9e7", "#019ff4", "#0300f4", "#02fd02", "#01c501",
                     "#008e00", "#fdf802", "#e5bc00", "#fd9500", "#fd0000",
                     "#d40000", "#bc0000", "#f800fd", "#9854c6", "#4c0099",]
precip_colormap = ListedColormap(nws_precip_colors)

def transform_from_latlon(lat, lon):
   lat = np.asarray(lat)
   lon = np.asarray(lon)
   trans = Affine.translation(lon[0],lat[0])
   scale = Affine.scale(lon[1] - lon[0], lat[1] - lat[0])
   return trans*scale

def rasterize(shapes, coords, latitude='latitude', longitude='longitude',
              fill1=np.nan, **kwargs):
   transform = transform_from_latlon(coords[latitude], coords[longitude])
   out_shape = (len(coords[latitude]), len(coords[longitude]))
   raster = features.rasterize(shapes, out_shape=out_shape,
                               fill=fill1,transform=transform,
                               dtype=float, all_touched=True,**kwargs)
   spatial_coords = {latitude: coords[latitude], longitude: coords[longitude]}
   return xr.DataArray(raster, coords=spatial_coords, dims=(latitude, longitude))

def add_shape_coord_from_data_array():
   shp_gpd = gpd.read_file('gz_2010_us_040_00_500k.json')
   shape = shp_gpd.query('NAME == "New York"')
   return shape

def make_nysm_map(etime,time1,dropzeros=True):
   precip = []
   for i in range(0,len(STN)):
      if (etime == 0):
         precip.append(np.nanmax(prcp_evol[i,0]))
      else:
         precip.append(np.nanmax(prcp_evol[i,0:etime]))

   if dropzeros:
       wh = [i for i, x in enumerate(precip) if x==0.]
       for i in reversed(wh): #needs to be reversed so we don't mess up the original indexing in the list
           del precip[i]
           del lons[i]
           del lats[i]
           del stns[i]
   nys = add_shape_coord_from_data_array()

   #plt.figure(figsize=(10,10))
   ax = gplt.polyplot(nys,facecolor='None',edgecolor='black',projection=gcrs.LambertConformal())
   levels = [0.,1.,2.,6.,10.,15.,20.,30.,40.,50.,70.,90.,110.,130.,150.,200.,300.]
   norm = BoundaryNorm(levels, 16)
   c1 = ax.scatter(lons, lats, c=precip,
         norm=norm,marker='o',s=200,
         transform=ccrs.PlateCarree(),
         zorder=2, alpha=1.,edgecolor='black',cmap=precip_colormap)
   cbar = plt.colorbar(c1, ticks=levels)
   cbar.set_label('Precipitation (mm)',rotation=90)
   plt.title(f'{str(time1.hour).zfill(2)} UTC {time1.day}-{time1.month}-{time1.year}',fontsize=18)

time1=datetime(2017,10,30,18)
etime = mtime.index(time1)
make_nysm_map(etime, time1)
plt.savefig(f'{time1.month}{time1.day}{str(time1.hour).zfill(2)}_accum_nysm.png',type='png',dpi=200)
plt.show()
#plt.close()






