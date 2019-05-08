# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 18:10:07 CET 2019
Last modified, Tue May  7 16:50:32 CEST 2019

 Copyright 2019 Didier M. Roche <didier.roche@lsce.ipsl.fr>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

@author: Didier M. Roche a.k.a. dmr
@author: Didier Paillard
"""

# Changes from version 0.0: Created the base code from the paper of Kottek et al., Meteorologische Zeitschrift, Vol. 15, No. 3, 259-263 (June 2006)

__version__ = "0.1"


# I will assume I have the necessary variables computed somewhere else

#~ T_min			Monthly mean T2m coldest month				(°C)
#~ T_max			Monthly mean T2m warmest month				(°C)
#~ T_mon			Monthly mean T2m of any month 				(°C)
#~ T_ann			Annual Mean T2m						(°C)
#~ P_min			Precipitation of the driest month				(mm/month)
#~ P_ann			Accumulated mean annual precipitation  			(mm/year)
#~ P_smin		lowest monthly precipitation for the summer half-year	(mm/month)
#~ P_smax		highest monthly precipitation for the summer half-year	(mm/month)
#~ P_wmin		lowest monthly precipitation for the winter half-year	(mm/month)
#~ P_wmax		highest monthly precipitation for the winter half-year	(mm/month)

def get_Equatorial_Climates(P_min,P_ann,P_smin,P_wmin,classification="") :

    if (P_min>60.0):
       classification+="f" # Equatorial rainforest, fully humid
    elif (P_ann>=25.0*(100.0-P_min)):
       classification+="m" # Equatorial monsoon
    elif (P_smin<=60.0):
       classification+="s" # Equatorial Savannah with dry summer
    elif (P_wmin<=60.0):
       classification+="w" # Equatorial Savannah with dry winter
    #endif
    return classification
#enddef get_Equatorial_Climates


def get_Arid_Climates(P_ann,P_th,T_ann):

    if P_ann > 5 * P_th:
       classification="S" # Steppe climate
    else:
       classification="W" # Desert climate
    #endif
    if T_ann >= 18.0:
       classification+="h" # Hot
    else:
       classification+="k" # cold
    #endif
    return classification
#enddef get_Arid_Climates

def get_Warm_Temp_Climates(P_smin,P_wmin,P_wmax,P_smax, T_max, T_min, T_mon):

    if P_smin < P_wmin and P_wmax > 3.0*P_smin and P_smin < 40.0:
       classification="s" # WTC, dry summers
    elif P_wmin < P_smin and P_smax > 10.0*P_wmin:
       classification="w" # WTC, dry winters
    else:
       classification="f" # WTC, fully humid
    #endif

    if T_max >= 22.0 :
       classification+="a" # Hot summer
    elif ma.sum(ma.masked_greater_equal(T_mon,10.0).mask) >= 4 : # Modification done
       classification+="b" # Warm summer
    elif T_min > -38.0 :
       classification+="c" # Cool summer and cold winter
    else:
       classification+="d" # extremely continental
    #endif

    return classification
#enddef get_Warm_Temp_Climates


def get_Snow_Climates(P_smin,P_smax,P_wmin,P_wmax, T_min, T_max,T_mon):

    if P_smin < P_wmin and P_wmax > 3.0*P_smin and P_smin < 40.0:
       classification="s" # SC, dry summers
    elif P_wmin < P_smin and P_smax > 10.0*P_wmin:
       classification="w" # SC, dry winters
    else:
       classification="f" # SC, fully humid
    #endif
    if T_max >= 22.0 :
       classification+="a" # Hot summer
    elif ma.sum(ma.masked_greater_equal(T_mon,10.0).mask) >= 4 : # Modification done
       classification+="b" # Warm summer
    elif T_min > -38.0 :
       classification+="c" # Cool summer and cold winter
    else:
       classification+="d" # extremely continental
    #endif

    return classification
#enddef get_Snow_Climates

def get_Polar_Climates(T_max):

    if T_max >= 0.0 :
       classification="T" # Tundra
    else:
       classification="F" # Frost
    #endif

    return classification
#enddef get_Snow_Climates

def get_kg_classification(T_min,T_max,T_mon,T_ann,P_min,P_ann,P_smin,P_smax,P_wmin,P_wmax,P_th):

    kg_classification=""

    if T_max < 10.0:
       kg_classification+="E"
       kg_classification+=get_Polar_Climates(T_max)
    elif P_ann < 10*P_th :
       kg_classification+="B"
       kg_classification+=get_Arid_Climates(P_ann,P_th,T_ann)
    elif T_min >= 18.0 :
       kg_classification+="A"
       kg_classification+=get_Equatorial_Climates(P_min,P_ann,P_smin,P_wmin)
    elif  -3.0 < T_min and T_min < 18.0 :
       kg_classification+="C"
       kg_classification+=get_Warm_Temp_Climates(P_smin,P_wmin,P_wmax,P_smax, T_max, T_min, T_mon)
    elif T_min <= -3.0 and T_max >= 10.0 :
       kg_classification+="D"
       kg_classification+=get_Snow_Climates(P_smin,P_smax,P_wmin,P_wmax,T_min, T_max,T_mon)
    else:
       kg_classification="F"
    #endif T_min

    return kg_classification
#enddef get_kg_classification


if __name__ == "__main__":

  print("This is Koeppen-Geiger classifications, version",__version__)

  import lcm_utils as lu

  import numpy as np
  from numpy import ma


  #~ import regriding_to as RT
  #~ var_temp = "tas"
  #~ varOut = RT.reGrid_to(tas_File,var_temp,prc_File,varForGrid=var_Grid,outFile="/home/roche/Soft-Devel/scripts/python/iloveclim-and-clim/tas_pcmdi-metrics_Amon_ERAINT_198901-200911-clim-GPCPGrid.nc")

  dataset = "CRU"

  if dataset == "ERA":

# ========== ERA-INTERIM

    tas_File = "era-interim_t2m_monmean_1979-1999.nc"
    prc_File = "era-interim_tp_monmean_1979-1999.nc"

    var_temp = "t2m"
    var_Grid = 'tp'

    liste_TAS, nc_TAS = lu.read_var_NC(tas_File,[var_temp,]) # returns a list, in K
    mon_TAS =  ma.masked_equal(liste_TAS[0],liste_TAS[0]._FillValue)-273.15
    lats = nc_TAS.variables['latitude']
    lons = nc_TAS.variables['longitude']
    plot_lats = lats

    liste_PRC, nc_PRC = lu.read_var_NC(prc_File,[var_Grid,]) # returns a list, in
    mon_PRC =  ma.masked_equal(liste_PRC[0],1e+20)*12000. # use a dummy value, no missing value in that file ...


# ==========
  elif dataset == "CRU":
# ========== CRU_TS / VASClimO

    tas_File = "cru_ts4.02.1951.2000.tmp.dat-ymonmean.nc"
    prc_File = "dataPrcpClim-ymonmean.nc"

    var_temp = "tmp"
    var_Grid = 'prcp'

    liste_PRC, nc_PRC = lu.read_var_NC(prc_File,[var_Grid,]) # returns a list, in
    mon_PRC =  ma.masked_equal(liste_PRC[0],liste_PRC[0]._FillValue)
    lats_PRC = nc_PRC.variables['Y']

    max_lats = lats_PRC[-1]
    min_lats = lats_PRC[0]

    liste_TAS, nc_TAS = lu.read_var_NC(tas_File,[var_temp,]) # returns a list, in K
    lats = nc_TAS.variables['lat']
    lons = nc_TAS.variables['lon']
    mon_TAS =  ma.masked_equal(liste_TAS[0],liste_TAS[0]._FillValue)[:,lu.find_closest(lats[:],min_lats):lu.find_closest(lats[:],max_lats)+1,:]
    plot_lats = lats[lu.find_closest(lats[:],min_lats):lu.find_closest(lats[:],max_lats)+1]

# ==========

  #end if on dataset

  T_min = ma.min( mon_TAS,axis=0)
  T_max = ma.max( mon_TAS,axis=0)
  T_ann = ma.mean(mon_TAS,axis=0)
  T_mon = mon_TAS

  P_min = ma.min( mon_PRC,axis=0)
  P_max = ma.max( mon_PRC,axis=0)
  P_ann = ma.sum(mon_PRC,axis=0)

  #lets define summer in northern hemisphere as 3->8 (april, september included)
  # lets find the index of the equator ...

  indx_equ = lu.find_closest(lats[:],0.0)

  P_smin = ma.zeros(mon_PRC[0,...].shape)
  P_smax = ma.zeros(mon_PRC[0,...].shape)
  P_ssum = ma.zeros(mon_PRC[0,...].shape)
  P_wmin = ma.zeros(mon_PRC[0,...].shape)
  P_wmax = ma.zeros(mon_PRC[0,...].shape)
  P_wsum = ma.zeros(mon_PRC[0,...].shape)


  if ( dataset == "ERA" ):

    # N_Summer / S_Winter
    # Northern Hemisphere
    P_smin[:indx_equ,:] = ma.min(mon_PRC[3:9,:indx_equ,:],axis=0)
    # Southern Hemisphere
    P_wmin[indx_equ:,:] = ma.min(mon_PRC[3:9,indx_equ:,:],axis=0)
    # Northern Hemisphere
    P_smax[:indx_equ,:] = ma.max(mon_PRC[3:9,:indx_equ,:],axis=0)
    # Southern Hemisphere
    P_wmax[indx_equ:,:] = ma.max(mon_PRC[3:9,indx_equ:,:],axis=0)
    # Northern Hemisphere
    P_ssum[:indx_equ,:] = ma.sum(mon_PRC[3:9,:indx_equ,:],axis=0)
    # Southern Hemisphere
    P_wsum[indx_equ:,:] = ma.sum(mon_PRC[3:9,indx_equ:,:],axis=0)

    # N_Winter / S_Summer
    # Northern Hemisphere
    P_wmin[:indx_equ,:] = ma.min(ma.concatenate((mon_PRC[-3:,:indx_equ,:],mon_PRC[:3,:indx_equ,:]),axis=0),axis=0)
    # Southern Hemisphere
    P_smin[indx_equ:,:] = ma.min(ma.concatenate((mon_PRC[-3:,indx_equ:,:],mon_PRC[:3,indx_equ:,:]),axis=0),axis=0)
    # Northern Hemisphere
    P_wmax[:indx_equ,:] = ma.max(ma.concatenate((mon_PRC[-3:,:indx_equ,:],mon_PRC[:3,:indx_equ,:]),axis=0),axis=0)
    # Southern Hemisphere
    P_smax[indx_equ:,:] = ma.max(ma.concatenate((mon_PRC[-3:,indx_equ:,:],mon_PRC[:3,indx_equ:,:]),axis=0),axis=0)
    # Northern Hemisphere
    P_wsum[:indx_equ,:] = ma.sum(ma.concatenate((mon_PRC[-3:,:indx_equ,:],mon_PRC[:3,:indx_equ,:]),axis=0),axis=0)
    # Southern Hemisphere
    P_ssum[indx_equ:,:] = ma.sum(ma.concatenate((mon_PRC[-3:,indx_equ:,:],mon_PRC[:3,indx_equ:,:]),axis=0),axis=0)

  elif ( dataset == "CRU" ):

    # N_Summer / S_Winter
    # Northern Hemisphere     indx_equ:
    P_smin[indx_equ:,:] = ma.min(mon_PRC[3:9,indx_equ:,:],axis=0)
    # Southern Hemisphere     :indx_equ
    P_wmin[:indx_equ,:] = ma.min(mon_PRC[3:9,:indx_equ,:],axis=0)
    # Northern Hemisphere
    P_smax[indx_equ:,:] = ma.max(mon_PRC[3:9,indx_equ:,:],axis=0)
    # Southern Hemisphere
    P_wmax[:indx_equ,:] = ma.max(mon_PRC[3:9,:indx_equ,:],axis=0)
    # Northern Hemisphere
    P_ssum[indx_equ:,:] = ma.sum(mon_PRC[3:9,indx_equ:,:],axis=0)
    # Southern Hemisphere
    P_wsum[:indx_equ,:] = ma.sum(mon_PRC[3:9,:indx_equ,:],axis=0)

    # N_Winter / S_Summer
    # Northern Hemisphere     indx_equ:
    P_wmin[indx_equ:,:] = ma.min(ma.concatenate((mon_PRC[-3:,indx_equ:,:],mon_PRC[:3,indx_equ:,:]),axis=0),axis=0)
    # Southern Hemisphere     :indx_equ
    P_smin[:indx_equ,:] = ma.min(ma.concatenate((mon_PRC[-3:,:indx_equ,:],mon_PRC[:3,:indx_equ,:]),axis=0),axis=0)
    # Northern Hemisphere
    P_wmax[indx_equ:,:] = ma.max(ma.concatenate((mon_PRC[-3:,indx_equ:,:],mon_PRC[:3,indx_equ:,:]),axis=0),axis=0)
    # Southern Hemisphere
    P_smax[:indx_equ,:] = ma.max(ma.concatenate((mon_PRC[-3:,:indx_equ,:],mon_PRC[:3,:indx_equ,:]),axis=0),axis=0)
    # Northern Hemisphere
    P_wsum[indx_equ:,:] = ma.sum(ma.concatenate((mon_PRC[-3:,indx_equ:,:],mon_PRC[:3,indx_equ:,:]),axis=0),axis=0)
    # Southern Hemisphere
    P_ssum[:indx_equ,:] = ma.sum(ma.concatenate((mon_PRC[-3:,:indx_equ,:],mon_PRC[:3,:indx_equ,:]),axis=0),axis=0)

  #end if

  #  Other version that includes finding the 6 warmest month ...
  # T_smooth = lu.smoothD(mon_TAS,window_len=6,window='flat')
  # np.roll(T_smooth[:,12,12],6)-T_smooth[:,12,12] gives the maximum difference (D.Paillard) of the shifted 6 months
  # np.argmax(np.roll(T_smooth[:,12,12],6)-T_smooth[:,12,12]) gives summer/winter month (2 before, 3 after)

  P_th = ma.zeros(mon_TAS[0,...].shape)

  P_wpro = P_wsum/P_ann
  P_spro = P_ssum/P_ann

  var_1 = ma.where(P_wpro>=2./3.,2.*T_ann,0.0)
  var_2 = ma.where(P_spro>=2./3.,2.*T_ann+28.0,0.0)

  P_th = ma.where((var_1 + var_2)<=0.0,2*T_ann+14.0,var_1+var_2)

  KG_map = ma.zeros(P_th.shape,np.int)
  KG_map.mask = (T_max.mask+P_max.mask)

  KG_dict = {
              "Af"  :  1,
              "Am"  :  2,
              "As"  :  3,
              "Aw"  :  4,
              "BWk" :  5,
              "BWh" :  6,
              "BSk" :  7,
              "BSh" :  8,
              "Cfa" :  9,
              "Cfb" : 10,
              "Cfc" : 11,
              "Csa" : 12,
              "Csb" : 13,
              "Csc" : 14,
              "Cwa" : 15,
              "Cwb" : 16,
              "Cwc" : 17,
              "Dfa" : 18,
              "Dfb" : 19,
              "Dfc" : 20,
              "Dfd" : 21,
              "Dsa" : 22,
              "Dsb" : 23,
              "Dsc" : 24,
              "Dsd" : 25,
              "Dwa" : 26,
              "Dwb" : 27,
              "Dwc" : 28,
              "Dwd" : 29,
              "EF"  : 30,
              "ET"  : 31
            }


  import progressbar as PB
  widgets = [PB.Bar('>'), ' ', PB.ETA(), ' ', PB.ReverseBar('<')]
  #~ widgets = [PB.SimpleProgress()]
  #~ widgets = ['Test: ', PB.Percentage(), ' ', PB.Bar(marker=PB.RotatingMarker()),' ', PB.ETA(), ' ', PB.FileTransferSpeed()]
  #~ widgets = [PB.Percentage(), PB.Bar()]

  pbar = PB.ProgressBar(widgets=widgets, maxval=P_th.shape[0]).start()

  if dataset == "ERA" : # not T_max.mask:
    for i in range(P_th.shape[0]):
        for j in range(P_th.shape[1]):
            lis_t = []
            KG_map[i,j] = KG_dict[get_kg_classification(T_min[i,j],T_max[i,j],T_mon[:,i,j],T_ann[i,j],P_min[i,j],P_ann[i,j],P_smin[i,j],P_smax[i,j],P_wmin[i,j],P_wmax[i,j],P_th[i,j])]
        #end for
        pbar.update(i)
    #end for
  else:
    for i in range(P_th.shape[0]):
        for j in range(P_th.shape[1]):
            if  not T_max.mask[i,j] and not P_min.mask[i,j] :
               lis_t = []
               KG_map[i,j] = KG_dict[get_kg_classification(T_min[i,j],T_max[i,j],T_mon[:,i,j],T_ann[i,j],P_min[i,j],P_ann[i,j],P_smin[i,j],P_smax[i,j],P_wmin[i,j],P_wmax[i,j],P_th[i,j])]
            #endif
        #end for
        pbar.update(i)
    #end for
  #end if

  pbar.finish()

  import matplotlib.pyplot as plt
  import cartopy.crs as ccrs

  #~ var2plot = ma.abs(KG_map-30)
  var2plot = KG_map

  #~ min_bounds = ma.min(var2plot)
  #~ max_bounds = ma.max(var2plot)
  #~ nbs_bounds = 30
  #~ fix_bounds = np.linspace(min_bounds,max_bounds,nbs_bounds)

  import create_KG_cmap as CKG
  the_chosen_map = CKG.KG_cmap_2006()

  fig = plt.figure(figsize=(10,10))
  ax = plt.axes(projection=ccrs.PlateCarree())

  mesh = ax.pcolormesh(lons[:], plot_lats[:], var2plot, cmap=the_chosen_map, transform=ccrs.PlateCarree())
  plt.colorbar(mesh, orientation='horizontal', shrink=0.75)
  ax.gridlines()
  ax.coastlines()

  #~ T_min  = -4.0
  #~ T_max  = 0.0
  #~ T_mon  = 0.0
  #~ T_ann  = 25.0
  #~ P_min  = 80.0
  #~ P_ann  = 24.0
  #~ P_smin = 0.0
  #~ P_smax = 0.0
  #~ P_wmin = 0.0
  #~ P_wmax = 0.0
  #~ P_th   = 1.0

  #~ print(get_kg_classification(T_min,T_max,T_mon,T_ann,P_min,P_ann,P_smin,P_smax,P_wmin,P_wmax,P_th))


#endif on main

# The End of All Things (op. cit.)
