# Correlations

import streamlit as st

import pandas as pd

import hvplot.pandas
import hvplot.xarray
import matplotlib.colors as mcolors
import holoviews as hv
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import geopandas as gpd

st.set_page_config(layout='wide')

# Customize the sidebar
st.sidebar.title('About')
st.sidebar.info('''
Author:\nDayan Renán Saynes Puma
''')

# Customize page title
st.title(':blue[Significant correlations]')

# Extract the rotated pole parameters
pole_lon = -186.0
pole_lat = 49.5

# Open the csv file that contains results of the teleconnection analysis on the NAO, EA, EAWR and SCA indices
fpath_telec = 'data/amax_pp_telec_reduced4colab.csv'
amax_pp_telec_df = pd.read_csv(fpath_telec, sep=';', encoding='latin-1')

# Convert the data frame to Xarray data set
amax_pp_telec_df.set_index(['rlat', 'rlon'], inplace=True) # this will convert "rlat" and "rlon" to dimensions in the new dataset
amax_pp_telec_ds = amax_pp_telec_df.to_xarray()

# Explore the shapefile that contains the catchment delimitations
#input_fpath_catchment = 'data/demarcaciones_a_terrestres/DEMARTER_16_21_2013.shp'
#catchments_init_proj = gpd.read_file(input_fpath_catchment)

# Explore the shapefile containing the rivers whose waters discharge into the Atlantinc Ocean
#input_fpath_atlant_river = 'data/rioscomppfafs/A_RiosCompletosv2.shp'
#atlant_rivers_init_proj = gpd.read_file(input_fpath_atlant_river)

# Explore the shapefile containing the rivers whose waters discharge into the Mediterranean Sea
#input_fpath_medit_river = 'data/rioscomppfafs/M_RiosCompletosv2.shp'
#medit_rivers_init_proj = gpd.read_file(input_fpath_medit_river)

# Reproject the data if necessary
# This aims to standardize the information
#catchments_ETRS89_30N_proj = catchments_init_proj.to_crs(epsg=25830)

# Filter rivers with orders 0 and 1
# this geo data frames will be useful in the maps
#rivers0_ETRS89_30N_proj = gpd.overlay(atlant_rivers_init_proj[atlant_rivers_init_proj['color']=='0'], medit_rivers_init_proj[medit_rivers_init_proj['color']=='0'], how='union')
#rivers1_ETRS89_30N_proj = gpd.overlay(atlant_rivers_init_proj[atlant_rivers_init_proj['color']=='1'], medit_rivers_init_proj[medit_rivers_init_proj['color']=='1'], how='union')

# Interactive plot for correlations

hv.extension('bokeh')

telec_lag0 = amax_pp_telec_ds.hvplot.quadmesh(x='rlon', y='rlat', z='pearson_xcorr_sig_lag0_aft', projection=ccrs.PlateCarree(), 
                                         crs=ccrs.RotatedPole(pole_longitude=pole_lon, pole_latitude=pole_lat),
                                         project=True, rasterize=True, 
                                         xlim=(-3, 8), ylim=(-4, 3), frame_width=400, frame_height=400, cmap='rainbow', clabel='Teleconnection code',
                                         features={'ocean': '50m', 'coastline': '50m'}, title='Lag-0', clim=(1, 15), tools=['hover'], hover_cols='all') # fontsize={'title': '10pt', 'ylabel': '5px', 'ticks': 20}

countries = gpd.read_file(shpreader.natural_earth('50m', 'cultural', 'admin_0_countries')).hvplot(geo=True, color='none')
#countries = gpd.read_file('https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/50m/cultural/ne_50m_admin_0_countries_lakes.zip').hvplot(geo=True, color='none')


# catchments = catchments_ETRS89_30N_proj.hvplot.polygons(geo=True, projection=ccrs.PlateCarree(), crs=ccrs.epsg(25830), color='none')
# rivers0 = rivers0_ETRS89_30N_proj.hvplot(geo=True, projection=ccrs.PlateCarree(), crs=ccrs.epsg(25830), color='royalblue', alpha=1)
# rivers1 = rivers1_ETRS89_30N_proj.hvplot(geo=True, projection=ccrs.PlateCarree(), crs=ccrs.epsg(25830), color='royalblue', alpha=1)

plot = telec_lag0*countries

st.bokeh_chart(hv.render(plot, backend='bokeh'))# use_container_width=True