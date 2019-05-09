# -*- coding: utf-8 -*-

"""
Created on Fri Jan 18 18:10:07 CET 2019
Last modified, Thu May  9 19:59:51 CEST 2019

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

# STD imports
import time

# Array imports
import numpy as np
from numpy import ma

# Plotting imports
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

# Regional utilities imports
import progressbar as PB
import lcm_utils as lu

# Local utilities imports
import create_KG_cmap as CKG


# Changes from version 0.0 : Created the base code from the paper of Kottek et al., Meteorologische Zeitschrift, Vol. 15, No. 3, 259-263 (June 2006)
# Changes from version 0.1 : Added the colorbar for reproducing the figures of Peel et al., Hydrol. Earth Syst. Sci., 11, 1633-1644, 2007
# Changes from version 0.2 : Added the second version of KG classifications, according to Peel et al., 2007
# Changes from version 0.3 : Added the third version of  KG classifications, according to Cannon, 2012
# Changes from version 0.4 : Restructured the main code to have a one-dimensional main call
# Changes from version 0.5 : Pre-computed the number of months > 10.0 to transmit less data in the main call. Performance improvement 40%
# Changes from version 0.60: Cleaned up unused variables and imports using pylint
# Changes from version 0.61: Cleaned up duplicate routines in Kottek & Peel versions
# Changes from version 0.62: Added the colormap of Cannon, Hydrol. Earth Syst. Sci., 16, 217-229, 2012
__version__ = "0.63"


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

def get_Equatorial_Climates_Kottek(P_min,P_ann,P_smin,P_wmin,classification="") :

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

def get_Equatorial_Climates_Peel(P_min,P_ann,classification="") :

    if (P_min>60.0):
       classification+="f" # Equatorial rainforest, fully humid
    elif (P_ann>=25.0*(100.0-P_min)):
       classification+="m" # Equatorial monsoon
    elif (P_min<=60.0):
       classification+="w" # Equatorial Savannah
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

def get_second_letter(P_smin,P_wmin,P_wmax,P_smax):
    if P_smin < P_wmin and P_wmax > 3.0*P_smin and P_smin < 40.0:
       classification="s" # WTC, dry summers
    elif P_wmin < P_smin and P_smax > 10.0*P_wmin:
       classification="w" # WTC, dry winters
    else:
       classification="f" # WTC, fully humid
    #endif
    return classification
# end def get_second_letter

def get_third_letter(T_max,T_mon,T_min):

    if T_max >= 22.0 :
       classification="a" # Hot summer
    elif T_mon >= 4 : # Modification done
       classification="b" # Warm summer
    elif T_min > -38.0 :
       classification="c" # Cool summer and cold winter
    else:
       classification="d" # extremely continental
    #endif

    return classification
# end def get_third_letter

def get_Second_Third_Letter(P_smin,P_wmin,P_wmax,P_smax, T_max, T_min, T_mon):

    classification = get_second_letter(P_smin,P_wmin,P_wmax,P_smax)

    classification += get_third_letter(T_max,T_mon,T_min)

    return classification
#enddef get_Second_Third_Letter

def get_Polar_Climates(T_max):

    if T_max >= 0.0 :
       classification="T" # Tundra
    else:
       classification="F" # Frost
    #endif

    return classification
#enddef get_Snow_Climates

def get_kg_classification(arguments, vers="peel"):

    T_min = arguments[0]
    T_max = arguments[1]
    T_mon = arguments[2]
    T_ann = arguments[3]
    P_min = arguments[4]
    P_ann = arguments[5]
    P_smin= arguments[6]
    P_smax= arguments[7]
    P_wmin= arguments[8]
    P_wmax= arguments[9]
    P_th  = arguments[10]

    kg_classification=""

    if T_max < 10.0:
       kg_classification+="E"
       kg_classification+=get_Polar_Climates(T_max)
    elif P_ann < 10*P_th :
       kg_classification+="B"
       kg_classification+=get_Arid_Climates(P_ann,P_th,T_ann)
    elif T_min >= 18.0 :
       kg_classification+="A"
       if vers == "kottek":
         kg_classification+=get_Equatorial_Climates_Kottek(P_min,P_ann,P_smin,P_wmin)
       else:
         kg_classification+=get_Equatorial_Climates_Peel(P_min,P_ann)
       #endif
    elif T_min > -3.0 and T_min < 18.0 :
       kg_classification+="C"
       kg_classification+=get_Second_Third_Letter(P_smin,P_wmin,P_wmax,P_smax, T_max, T_min, T_mon)
    elif T_min <= -3.0 and T_max >= 10.0 :
       kg_classification+="D"
       kg_classification+=get_Second_Third_Letter(P_smin,P_wmin,P_wmax,P_smax, T_max, T_min, T_mon)
    else:
       kg_classification="F"
    #endif T_min

    return kg_classification
#enddef get_kg_classification

def get_kg_classification_Cannon(arguments):

    T_min = arguments[0]
    T_max = arguments[1]
    T_mon = arguments[2]
    T_ann = arguments[3]
    P_min = arguments[4]
    P_ann = arguments[5]
    P_smin= arguments[6]
    P_smax= arguments[7]
    P_wmin= arguments[8]
    P_wmax= arguments[9]
    P_th  = arguments[10]

    kg_classification=""

    if T_ann >= 12.0:
        if P_ann >= 1400.0 :
            if P_min >= 70.0:
               if P_ann >= 2800.0:
                   if P_ann >= 3700.0:
                       kg_classification="1WW"
                   else:
                       kg_classification="1WD"
                   #endif
               else: # P_ann < 2800
                   if P_ann > 2000.0:
                       kg_classification="1DW"
                   else:
                       kg_classification="1DD"
                   #endif
               #endif # on P_ann > 2800
            else: # P_min < 70
               if P_ann >= 2200.0:

                   if P_smax >= 590.0:
                       kg_classification="2Ww"
                   else:
                       kg_classification="2Wd"
                   #endif

               else: # P_ann < 2200
                   if P_min > 30.0:
                       if T_min >= 16.0:
                           kg_classification="2Dh"
                       else:
                           kg_classification="2Dc"
                       #endif
                   else: # P_min < 30
                       if P_wmax >= 170.0:
                           kg_classification="2Dw"
                       else:
                           kg_classification="2Dd"
                       #endif
                   #endif # on P_min > 30
               #endif # on P_ann > 2200
            # endif on P_min
        else: # P_ann < 1400
            if P_ann >= 600.0:
                if T_min >= 14.0:
                    if T_max >= 30.0:
                        kg_classification="3hh"
                    else:
                        if P_ann >= 1000.0:
                            kg_classification="3hW"
                        else:
                            kg_classification="3hD"
                        #endif
                    #endif on T_max >= 30
                else: # T_min < 14
                    if P_wmin >= 40.0:
                        kg_classification="3cw"
                    else:
                        kg_classification="3cd"
                    #endif
                #endif
            else: # P_ann < 600.0
                if T_ann >= 22:
                    if P_smax >= 60.0 :
                        kg_classification="3Hw"
                    else:
                        kg_classification="3Hd"
                    #endif P_smax >= 60
                else: # T_ann < 22
                    if T_ann >= 18.0:
                        kg_classification="3CH"
                    else: # T_ann < 18
                        kg_classification="3CC"
                    #endif
                #endif on T_ann >= 22
            #endif on P_ann >= 600
        #endif on P_ann >= 1400
    else: # T_ann < 12
        if T_ann >= -2.0:
            if P_wmax >= 110.0:
                if P_wmax >= 230:
                    kg_classification="4Ww"
                else:
                    kg_classification="4Wd"
                #endif
            else: # P_wmax < 110
                if T_ann >= 5:
                    if P_ann >= 500:
                        kg_classification="4HW"
                    else:
                        kg_classification="4HD"
                    #endif
                else: # T_ann < 5
                    if T_max >= 16.0:
                        kg_classification="4Ch"
                    else:
                        kg_classification="4Cc"
                    #endif
                #endif on T_ann >= 5
            #endif P_wmax >= 110
        else: #T_ann < -2.0
            if T_max >= 5:
                if T_ann >= -9:
                    if T_max >= 13:
                        kg_classification="5hh"
                    else:
                        kg_classification="5hc"
                    #endif on T_max >= 13
                else: # T_ann < -9
                    kg_classification="5hC"
                #endif T_ann >= -9
            else: # T_max < 5
                if P_min >= 50:
                    kg_classification="5cw"
                else:
                    kg_classification="5cd"
                #endif
            #endif on T_max >= 5
        #endif on T_ann >= -2
    #endif on T_ann >= 12
    return kg_classification
#enddef get_kg_classification_Cannon


if __name__ == "__main__":

  print("This is Koeppen-Geiger classifications, version",__version__)

  #~ import regriding_to as RT
  #~ var_temp = "tas"
  #~ varOut = RT.reGrid_to(tas_File,var_temp,prc_File,varForGrid=var_Grid,outFile="/home/roche/Soft-Devel/scripts/python/iloveclim-and-clim/tas_pcmdi-metrics_Amon_ERAINT_198901-200911-clim-GPCPGrid.nc")

  dataset = "CRU"

  if dataset == "ERA":

# ========== ERA-INTERIM

    tas_File = "test-data/era-interim_t2m_monmean_1979-1999.nc"
    prc_File = "test-data/era-interim_tp_monmean_1979-1999.nc"

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

    tas_File = "test-data/cru_ts4.02.1951.2000.tmp.dat-ymonmean.nc"
    prc_File = "test-data/dataPrcpClim-ymonmean.nc"

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

  T_mon = ma.sum(ma.masked_greater_equal(mon_TAS,10.0).mask,axis=0) # T_mon no longer contains Monthly Temp.

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
  KG_map.mask =  True # (T_max.mask+P_max.mask)

  KG_dict, the_chosen_map = CKG.KG_cmap_2007()

  #~ widgets = [PB.Bar('>'), ' ', PB.ETA(), ' ', PB.ReverseBar('<')]
  #~ widgets = [PB.SimpleProgress()]
  #~ widgets = ['Test: ', PB.Percentage(), ' ', PB.Bar(marker=PB.RotatingMarker()),' ', PB.ETA(), ' ', PB.FileTransferSpeed()]
  widgets = [PB.Percentage(), PB.Bar()]

  init_shape = T_min.shape

  Asize = T_min.size

  ARGS = ma.zeros((11,Asize))

  ARGS[0,:]  = T_min.flatten()
  ARGS[1,:]  = T_max.flatten()
  ARGS[2,:]  = T_mon.flatten()
  ARGS[3,:]  = T_ann.flatten()
  ARGS[4,:]  = P_min.flatten()
  ARGS[5,:]  = P_ann.flatten()
  ARGS[6,:]  = P_smin.flatten()
  ARGS[7,:]  = P_smax.flatten()
  ARGS[8,:]  = P_wmin.flatten()
  ARGS[9,:]  = P_wmax.flatten()
  ARGS[10,:] = P_th.flatten()

  KG_MAP = KG_map.flatten()

  pbar = PB.ProgressBar(widgets=widgets, maxval=Asize).start()

  start_time = time.time()

  #~ for i in range(Asize):
      #~ if  not ARGS.mask[4,i] and not ARGS.mask[0,i] :
          #~ KG_MAP[i] = KG_dict[get_kg_classification(ARGS[:,i])]
      #~ #endif
      #~ pbar.update(i)
  #~ #end for

  for i in range(Asize):
      if  not ARGS.mask[4,i] and not ARGS.mask[0,i] :
          KG_MAP[i] = KG_dict[get_kg_classification(ARGS[:,i],vers="peel")]
      #~ KG_MAP[i] = KG_dict[get_kg_classification_Cannon(ARGS[:,i])]
      #endif
      pbar.update(i)
  #end for

  KG_map = KG_MAP.reshape(init_shape)

  pbar.finish()

  print("--- %s seconds ---" % (time.time() - start_time))

  var2plot = KG_map

  fig = plt.figure(figsize=(10,10))
  ax = plt.axes(projection=ccrs.PlateCarree())

  mesh = ax.pcolormesh(lons[:], plot_lats[:], var2plot, cmap=the_chosen_map, transform=ccrs.PlateCarree())
  plt.colorbar(mesh, orientation='horizontal', shrink=0.75)
  ax.gridlines()
  ax.coastlines()

#endif on main

# The End of All Things (op. cit.)
