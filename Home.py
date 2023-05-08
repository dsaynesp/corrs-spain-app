# Correlations and significant non-stationarities over Spain

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
The content of this web application corresponds to partial results of the master thesis **_Non-stationary frequency analysis of extreme precipitation in Spain for its prediction in climate change scenarios_**.\n
Author:\nDayan Renán Saynes Puma (dsaypum@posgrado.upv.es)\n
Advisor:\nFélix Francés García (ffrances@upv.es)
''')

# Customize page title
st.title(':blue[Correlations and significant non-stationarities over Spain]')

st.markdown('''
The interactive maps show the results of the analysis of teleconnections and non-stationarities in the period 10/1951-09/2020 (69 hydrological years) over mainland Spain and the Balearic Islands.

The data were provided by [AEMET](https://www.aemet.es/es/serviciosclimaticos/cambio_climat/datos_diarios?w=2&w2=0) in gridded format (rotated) and have a daily temporal resolution and 0.05 degrees of spatial resolution.

**1.  Teleconnections:** Pearson correlations significant up to 2 lags between Annual Maximum Daily Precipitation and winter-averaged climate indices NAO, EA, EAWR and SCA, under a local significance level of 0.05. The graphical representation of these results is by cells. Each cell has a color linked to a code between 1 and 15.

  * Meaning of the codes: `1: NAO`, `2: EA`, `3: EAWR`, `4: SCA`, `5: NAO-EA`, `6: NAO-EAWR`, `7: NAO-SCA`, `8: EA-EAWR`, `9: EA-SCA`, `10: EAWR-SCA`, `11: NAO-EA-EAWR`, `12: NAO-EAWR-SCA`, `13: NAO-EA-SCA`, `14: EA-EAWR-SCA`, `15: NAO-EA-EAWR-SCA`.

**2.  Non-stationarities:** Significant change points and trends identified by Pettitt and modified Mann-Kendall (Hamed and Rao, 1995) tests. Statistical significance was evaluated at both local (maps in the first column) and global (maps in the second column) level. The graphical representation of these results is by points. Each point has a color linked to a code between 1 and 3.

  * Meaning of the codes: `1: Change point`, `2: Trend`, `3: Change point and trend`.
'''
)

# Extract the rotated pole parameters
pole_lon = -186.0
pole_lat = 49.5

# Open the csv file that contains results of the non-stationarity analysis
fpath_test = 'data/amax_pp_test_reduced4colab.csv'
amax_pp_test_df = pd.read_csv(fpath_test, sep=';', encoding='latin-1')

nonstat_mk_orig_df = amax_pp_test_df[['rlon', 'rlat', 'lon', 'lat', 'nonstat_mk_orig']]
nonstat_mk_orig_df = nonstat_mk_orig_df[nonstat_mk_orig_df['nonstat_mk_orig']!=0]

nonstat_mk_orig_BH_df = amax_pp_test_df[['rlon', 'rlat', 'lon', 'lat', 'nonstat_mk_orig_BH']]
nonstat_mk_orig_BH_df = nonstat_mk_orig_BH_df[nonstat_mk_orig_BH_df['nonstat_mk_orig_BH']!=0]

nonstat_mk_HR_df = amax_pp_test_df[['rlon', 'rlat', 'lon', 'lat', 'nonstat_mk_HR']]
nonstat_mk_HR_df = nonstat_mk_HR_df[nonstat_mk_HR_df['nonstat_mk_HR']!=0]

nonstat_mk_HR_BH_df = amax_pp_test_df[['rlon', 'rlat', 'lon', 'lat', 'nonstat_mk_HR_BH']]
nonstat_mk_HR_BH_df = nonstat_mk_HR_BH_df[nonstat_mk_HR_BH_df['nonstat_mk_HR_BH']!=0]

# Convert the previously created data frames into geo data frames
nonstat_mk_orig_gdf = gpd.GeoDataFrame(nonstat_mk_orig_df, geometry=gpd.points_from_xy(nonstat_mk_orig_df['rlon'], nonstat_mk_orig_df['rlat']), 
                                       crs=ccrs.RotatedPole(pole_longitude=pole_lon, pole_latitude=pole_lat))
nonstat_mk_orig_BH_gdf = gpd.GeoDataFrame(nonstat_mk_orig_BH_df, geometry=gpd.points_from_xy(nonstat_mk_orig_BH_df['rlon'], nonstat_mk_orig_BH_df['rlat']), 
                                          crs=ccrs.RotatedPole(pole_longitude=pole_lon, pole_latitude=pole_lat))
nonstat_mk_HR_gdf = gpd.GeoDataFrame(nonstat_mk_HR_df, geometry=gpd.points_from_xy(nonstat_mk_HR_df['rlon'], nonstat_mk_HR_df['rlat']), 
                                     crs=ccrs.RotatedPole(pole_longitude=pole_lon, pole_latitude=pole_lat))
nonstat_mk_HR_BH_gdf = gpd.GeoDataFrame(nonstat_mk_HR_BH_df, geometry=gpd.points_from_xy(nonstat_mk_HR_BH_df['rlon'], nonstat_mk_HR_BH_df['rlat']), 
                                        crs=ccrs.RotatedPole(pole_longitude=pole_lon, pole_latitude=pole_lat))

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

# Make an interactive plot for correlations and significant non-stationarities

hv.extension('bokeh')

#cmap_nonstat = mcolors.ListedColormap(['blue', 'red', 'black'])

telec_lag0 = amax_pp_telec_ds.hvplot.quadmesh(x='rlon', y='rlat', z='pearson_xcorr_sig_lag0_aft', projection=ccrs.PlateCarree(), 
                                         crs=ccrs.RotatedPole(pole_longitude=pole_lon, pole_latitude=pole_lat),
                                         project=True, rasterize=True, 
                                         xlim=(-3, 8), ylim=(-4, 3), frame_width=400, frame_height=400, cmap='rainbow', clabel='Teleconnection code',
                                         features={'ocean': '50m', 'coastline': '50m'}, title='Lag-0', clim=(1, 15), tools=['hover'], hover_cols='all') # fontsize={'title': '10pt', 'ylabel': '5px', 'ticks': 20}

#telec_lag1 = amax_pp_telec_ds.hvplot.quadmesh(x='rlon', y='rlat', z='pearson_xcorr_sig_lag1_aft', projection=ccrs.PlateCarree(), 
#                                         crs=ccrs.RotatedPole(pole_longitude=pole_lon, pole_latitude=pole_lat), 
#                                         project=True, rasterize=True,
#                                         xlim=(-3, 8), ylim=(-4, 3), frame_width=400, frame_height=400, cmap='rainbow', clabel='Teleconnection code',
#                                         features={'ocean': '50m', 'coastline': '50m'}, title='Lag-1', clim=(1, 15), tools=['hover'], hover_cols='all')

#telec_lag2 = amax_pp_telec_ds.hvplot.quadmesh(x='rlon', y='rlat', z='pearson_xcorr_sig_lag2_aft', projection=ccrs.PlateCarree(), 
#                                         crs=ccrs.RotatedPole(pole_longitude=pole_lon, pole_latitude=pole_lat), 
#                                         project=True, rasterize=True,
#                                         xlim=(-3, 8), ylim=(-4, 3), frame_width=400, frame_height=400, cmap='rainbow', clabel='Teleconnection code',
#                                         features={'ocean': '50m', 'coastline': '50m'}, title='Lag-2', clim=(1, 15), tools=['hover'], hover_cols='all')

#nonstat_mk_HR = nonstat_mk_HR_gdf.hvplot(geo=True, projection=ccrs.PlateCarree(), 
#                         crs=ccrs.RotatedPole(pole_longitude=pole_lon, pole_latitude=pole_lat), 
#                         c='nonstat_mk_HR', cmap=cmap_nonstat, alpha=0.6, hover_cols='all', use_index=False, colorbar=False)

#nonstat_mk_HR_BH = nonstat_mk_HR_BH_gdf.hvplot(geo=True, projection=ccrs.PlateCarree(), 
#                         crs=ccrs.RotatedPole(pole_longitude=pole_lon, pole_latitude=pole_lat), 
#                         c='nonstat_mk_HR_BH', cmap=cmap_nonstat, alpha=0.6, hover_cols='all', use_index=False, colorbar=False)

#countries = gpd.read_file(shpreader.natural_earth('50m', 'cultural', 'admin_0_countries')).hvplot(geo=True, color='none')

# catchments = catchments_ETRS89_30N_proj.hvplot.polygons(geo=True, projection=ccrs.PlateCarree(), crs=ccrs.epsg(25830), color='none')
# rivers0 = rivers0_ETRS89_30N_proj.hvplot(geo=True, projection=ccrs.PlateCarree(), crs=ccrs.epsg(25830), color='royalblue', alpha=1)
# rivers1 = rivers1_ETRS89_30N_proj.hvplot(geo=True, projection=ccrs.PlateCarree(), crs=ccrs.epsg(25830), color='royalblue', alpha=1)

#plot = (telec_lag0*nonstat_mk_HR*countries + telec_lag0*nonstat_mk_HR_BH*countries +
#        telec_lag1*nonstat_mk_HR*countries + telec_lag1*nonstat_mk_HR_BH*countries +
#        telec_lag2*nonstat_mk_HR*countries + telec_lag2*nonstat_mk_HR_BH*countries).cols(2)
#plot=telec_lag0*nonstat_mk_HR*countries
plot=telec_lag0

st.bokeh_chart(hv.render(plot, backend='bokeh'))# use_container_width=True