# -*- coding: utf-8 -*-

"""
Created on Fri Jan 18 18:10:07 CET 2019
Last modified, Fri Feb 18 16:23:56 CET 2022

 Copyright 2019-2022 Didier M. Roche <didier.roche@lsce.ipsl.fr>

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at
 
     http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.

@author: Didier M. Roche a.k.a. dmr
@author: Didier Paillard
"""

# STD imports
import time

# Array imports
from typing import Any, Union, Iterable

import numpy as np
from numpy import ma

# Plotting imports
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

# Regional utilities imports
import sys
path_to_module = "/tertiaire/backup/014_lsce3027-2020-06-25/Soft-Devel/scripts/python"

sys.path.append(path_to_module)
path_to_module = "/tertiaire/backup/014_lsce3027-2020-06-25/Soft-Devel/scripts/python/python-progressbar"
sys.path.append(path_to_module)

import progressbar as PB
import lcm_utils as lu

# Local utilities imports
from numpy.core._multiarray_umath import ndarray

import create_KG_cmap as CKG

# Changes from version 0.0 : Created the base code from the paper of Kottek et al., Meteorologische Zeitschrift, Vol. 15, No. 3, 259-263 (June 2006)
# Changes from version 0.1 : Added the colorbar for reproducing the figures of Peel et al., Hydrol. Earth Syst. Sci., 11, 1633-1644, 2007
# Changes from version 0.2 : Added the second version of KG classifications, according to Peel et al., 2007
# Changes from version 0.3 : Added the third version of  KG classifications, according to Cannon, 2012
# Changes from version 0.4 : Restructured the main code to have a one-dimensional main call
# Changes from version 0.5 : Pre-computed the number of months > 10.0 to transmit less data in the main call. Performance improvement 40%
# Changes from version 0.60: Cleaned up unused variables and imports using pylint
# Changes from version 0.61: Cleaned up duplicate routines in Kottek & Peel versions
# Changes from version 0.62: Added the colormap of Cannon, Hydrol. Earth Syst. Sci., 16, 217-229, 2012
# Changes from version 0.63: Modified the computation of summer / winter indicies with generality in mind
# Changes from version 0.64: cleaned up the code, removing unnecessary bits
# Changes from version 0.65: refactored part of the code, added Trewartha, automatic labelling of the bioclimatic zones
# Changes from version 0.75: refactored part of the code, added match/case for the different classifications

__version__ = "0.80"


# I will assume I have the necessary variables computed somewhere else

# ~ T_min			Monthly mean T2m coldest month				( C)
# ~ T_max			Monthly mean T2m warmest month				( C)
# ~ T_mon			Monthly mean T2m of any month 				( C)
# ~ T_ann			Annual Mean T2m						( C)
# ~ P_min			Precipitation of the driest month				(mm/month)
# ~ P_ann			Accumulated mean annual precipitation  			(mm/year)
# ~ P_smin		lowest monthly precipitation for the summer half-year	(mm/month)
# ~ P_smax		highest monthly precipitation for the summer half-year	(mm/month)
# ~ P_wmin		lowest monthly precipitation for the winter half-year	(mm/month)
# ~ P_wmax		highest monthly precipitation for the winter half-year	(mm/month)
# ~ P_wpro      
# ~ P_dry

def get_Equatorial_Climates_Kottek(P_min,P_ann,P_smin,P_wmin,classification="") :

    if (P_min > 60.0):
        classification += "f"  # Equatorial rainforest, fully humid
    elif (P_ann >= 25.0 * (100.0 - P_min)):
        classification += "m"  # Equatorial monsoon
    elif (P_smin <= 60.0):
        classification += "s"  # Equatorial Savannah with dry summer
    elif (P_wmin <= 60.0):
        classification += "w"  # Equatorial Savannah with dry winter
    # endif
    return classification
#enddef get_Equatorial_Climates_Kottek

def get_Equatorial_Climates_Peel(P_min,P_ann,classification="") :

    if (P_min > 60.0):
        classification += "f"  # Equatorial rainforest, fully humid
    elif (P_ann >= 25.0 * (100.0 - P_min)):
        classification += "m"  #  Equatorial monsoon
    elif (P_min <= 60.0):
        classification += "w"  # Equatorial Savannah
    # endif
    return classification
#enddef get_Equatorial_Climates_Peel

def get_Arid_Climates(P_ann,P_th,T_ann):

    if P_ann > 5 * P_th:
        classification = "S"  # Steppe climate
    else:
        classification = "W"  # Desert climate
    # endif
    if T_ann >= 18.0:
        classification += "h"  # Hot
    else:
        classification += "k"  # cold
    # endif
    return classification
#enddef get_Arid_Climates

def get_second_letter(P_smin,P_wmin,P_wmax,P_smax):
    if P_smin < P_wmin and P_wmax > 3.0 * P_smin and P_smin < 40.0:
        classification = "s"  # WTC, dry summers
    elif P_wmin < P_smin and P_smax > 10.0 * P_wmin:
        classification = "w"  # WTC, dry winters
    else:
        classification = "f"  # WTC, fully humid
    # endif
    return classification
# end def get_second_letter

def get_third_letter(T_max,T_mon,T_min):

    if T_max >= 22.0:
        classification = "a"  # Hot summer
    elif T_mon >= 4:  # Modification done
        classification = "b"  # Warm summer
    elif T_min > -38.0:
        classification = "c"  # Cool summer and cold winter
    else:
        classification = "d"  # extremely continental
    # endif

    return classification
# end def get_third_letter

def get_Second_Third_Letter(P_smin,P_wmin,P_wmax,P_smax, T_max, T_min, T_mon):

    classification = get_second_letter(P_smin,P_wmin,P_wmax,P_smax)

    classification += get_third_letter(T_max,T_mon,T_min)

    return classification
# enddef get_Second_Third_Letter

def get_Polar_Climates(T_max):

    if T_max >= 0.0:
        classification = "T"  # Tundra
    else:
        classification = "F"  #  Frost
    # endif

    return classification
# enddef get_Snow_Climates

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
        kg_classification += "E"
        kg_classification += get_Polar_Climates(T_max)
    elif P_ann < 10 * P_th:
        kg_classification += "B"
        kg_classification += get_Arid_Climates(P_ann, P_th, T_ann)
    elif T_min >= 18.0:
        kg_classification += "A"
        if vers == "kottek":
            kg_classification += get_Equatorial_Climates_Kottek(P_min, P_ann, P_smin, P_wmin)
        else:
            kg_classification += get_Equatorial_Climates_Peel(P_min, P_ann)
        # endif
    elif T_min > -3.0 and T_min < 18.0:
        kg_classification += "C"
        kg_classification += get_Second_Third_Letter(P_smin, P_wmin, P_wmax, P_smax, T_max, T_min, T_mon)
    elif T_min <= -3.0 and T_max >= 10.0:
        kg_classification += "D"
        kg_classification += get_Second_Third_Letter(P_smin, P_wmin, P_wmax, P_smax, T_max, T_min, T_mon)
    else:
        kg_classification = "F"
    # endif T_min

    return kg_classification
# enddef get_kg_classification

def get_kg_classification_Trewartha(arguments, vers="trewartha"):
    T_min = arguments[0]
    T_max = arguments[1]
    T_mon = arguments[2]
    T_ann = arguments[3]
    P_min = arguments[4]
    P_ann = arguments[5]
    P_smin = arguments[6]
    P_smax = arguments[7]
    P_wmin = arguments[8]
    P_wmax = arguments[9]
    P_wpro = arguments[11]
    P_dry = arguments[12]

    kg_classification = ""

    A = 2.3*T_ann-0.64*P_wpro+41

    if T_max < 0.0:
        kg_classification += "Fi"
    elif T_max < 10.0:
        kg_classification += "Ft"
    elif T_mon <= 3:
        if T_min <= -10.0:
            kg_classification += "Ec"
        else:
            kg_classification += "Eo"
        # endif on T_min
    elif T_mon <= 7:
        if T_min <= 0.0:
            kg_classification += "Dc"
        else:
            kg_classification += "Do"
        # endif on T_min
    elif T_min > 18.0 and P_ann/10.0 > A :
        # Climates Ar and Aw, with or without dry season
        if P_dry < 3:
            kg_classification += "Ar"
        else:
            kg_classification += "Aw"
        pass
    elif T_mon >= 8.0 and P_ann/10.0 > A : # and P_ann < 890.0 
        if P_smin < 30.0 and P_min < 1. / 3. * P_wmax:
            kg_classification += "Cs"
        elif P_smax > 10.0 * P_wmin:
            kg_classification += "Cw"
        else:
            kg_classification += "Cr"
        # endif on precipitation
    else:
        if P_ann/10.0 <= 0.5 * A :
            kg_classification += "BW"
        else:
            kg_classification += "BS"
    # endif T_min

    return kg_classification


# enddef get_kg_classification_Trewartha


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
        if P_ann >= 1400.0:
            if P_min >= 70.0:
                if P_ann >= 2800.0:
                    if P_ann >= 3700.0:
                        kg_classification = "1WW"
                    else:
                        kg_classification = "1WD"
                    # endif
                else:  # P_ann < 2800
                    if P_ann > 2000.0:
                        kg_classification = "1DW"
                    else:
                        kg_classification = "1DD"
                    # endif
                # endif on P_ann > 2800
            else:  # P_min < 70
                if P_ann >= 2200.0:

                    if P_smax >= 590.0:
                        kg_classification = "2Ww"
                    else:
                        kg_classification = "2Wd"
                    # endif

                else:  # P_ann < 2200
                    if P_min > 30.0:
                        if T_min >= 16.0:
                            kg_classification = "2Dh"
                        else:
                            kg_classification = "2Dc"
                        # endif
                    else:  # P_min < 30
                        if P_wmax >= 170.0:
                            kg_classification = "2Dw"
                        else:
                            kg_classification = "2Dd"
                        # endif
                    # endif on P_min > 30
                # endif on P_ann > 2200
            # endif on P_min
        else:  # P_ann < 1400
            if P_ann >= 600.0:
                if T_min >= 14.0:
                    if T_max >= 30.0:
                        kg_classification="3hh"
                    else:
                        if P_ann >= 1000.0:
                            kg_classification="3hW"
                        else:
                            kg_classification="3hD"
                        # endif
                    # endif on T_max >= 30
                else:  # T_min < 14
                    if P_wmin >= 40.0:
                        kg_classification = "3cw"
                    else:
                        kg_classification = "3cd"
                    # endif
                # endif
            else:  # P_ann < 600.0
                if T_ann >= 22:
                    if P_smax >= 60.0:
                        kg_classification = "3Hw"
                    else:
                        kg_classification = "3Hd"
                    # endif P_smax >= 60
                else:  # T_ann < 22
                    if T_ann >= 18.0:
                        kg_classification = "3CH"
                    else:  # T_ann < 18
                        kg_classification = "3CC"
                    # endif
                # endif on T_ann >= 22
            # endif on P_ann >= 600
        # endif on P_ann >= 1400
    else:  # T_ann < 12
        if T_ann >= -2.0:
            if P_wmax >= 110.0:
                if P_wmax >= 230:
                    kg_classification = "4Ww"
                else:
                    kg_classification = "4Wd"
                # endif
            else:  # P_wmax < 110
                if T_ann >= 5:
                    if P_ann >= 500:
                        kg_classification = "4HW"
                    else:
                        kg_classification = "4HD"
                    # endif
                else:  # T_ann < 5
                    if T_max >= 16.0:
                        kg_classification = "4Ch"
                    else:
                        kg_classification = "4Cc"
                    # endif
                # endif on T_ann >= 5
            # endif P_wmax >= 110
        else:  # T_ann < -2.0
            if T_max >= 5:
                if T_ann >= -9:
                    if T_max >= 13:
                        kg_classification = "5hh"
                    else:
                        kg_classification = "5hc"
                    # endif on T_max >= 13
                else:  # T_ann < -9
                    kg_classification = "5hC"
                # endif T_ann >= -9
            else:  # T_max < 5
                if P_min >= 50:
                    kg_classification = "5cw"
                else:
                    kg_classification = "5cd"
                # endif
            # endif on T_max >= 5
        # endif on T_ann >= -2
    # endif on T_ann >= 12
    return kg_classification
# enddef get_kg_classification_Cannon

def get_maxminsum_Slice(mon_var, indx_l=None, indx_h=None):
    """

    Parameters
    ----------
    mon_var :
    """
    # obtain a variable with size 24 at first index, 11 or 23 is december, 0 or 12 is january
    repeatedVar = np.r_[mon_var, mon_var]
    slicedVar = repeatedVar[12 + indx_l:12 + indx_h, ...]
    return ma.max(slicedVar, axis=0), ma.min(slicedVar, axis=0), ma.sum(slicedVar, axis=0)


# end def get_maxminsum_Slice

def exchange_tabs(arr_a, arr_b):
    arr_c = arr_b
    arr_b = arr_a
    arr_a = arr_c

    del (arr_c)
    return
# end def exchange_tabs


if __name__ == "__main__":
	
    typ_classification = "trewartha"

    print("This is Koeppen-Geiger classifications, version", __version__, "type == ", typ_classification)

    # ~ import regriding_to as RT
    # ~ var_temp = "tas"
    # ~ varOut = RT.reGrid_to(tas_File,var_temp,prc_File,varForGrid=var_Grid,outFile="/home/roche/Soft-Devel/scripts/python/iloveclim-and-clim/tas_pcmdi-metrics_Amon_ERAINT_198901-200911-clim-GPCPGrid.nc")

    dataset = "CRU"

    if dataset == "ERA":

        # ========== ERA-INTERIM

        tas_File = "test-data/era-interim_t2m_monmean_1979-1999.nc"
        prc_File = "test-data/era-interim_tp_monmean_1979-1999.nc"

        var_temp = "t2m"
        var_Grid = 'tp'

        liste_TAS, nc_TAS = lu.read_var_NC(tas_File, [var_temp, ])  # returns a list, in K
        mon_TAS = ma.masked_equal(liste_TAS[0], liste_TAS[0]._FillValue) - 273.15
        lats = nc_TAS.variables['latitude']
        lons = nc_TAS.variables['longitude']
        plot_lats = lats

        liste_PRC, nc_PRC = lu.read_var_NC(prc_File, [var_Grid, ])  # returns a list, in
        mon_PRC = ma.masked_equal(liste_PRC[0], 1e+20) * 12000.  # use a dummy value, no missing value in that file ...


    # ==========
    elif dataset == "CRU":
        # ========== CRU_TS / VASClimO

        tas_File = "test-data/cru_ts4.02.1951.2000.tmp.dat-ymonmean.nc"
        prc_File = "test-data/dataPrcpClim-ymonmean.nc"

        var_temp = "tmp"
        var_Grid = 'prcp'

        liste_PRC, nc_PRC = lu.read_var_NC(prc_File, [var_Grid, ])  # returns a list, in
        mon_PRC = ma.masked_equal(liste_PRC[0], liste_PRC[0]._FillValue)
        lats_PRC = nc_PRC.variables['Y']

        max_lats = lats_PRC[-1]
        min_lats = lats_PRC[0]

        liste_TAS, nc_TAS = lu.read_var_NC(tas_File, [var_temp, ])  # returns a list, in K
        lats = nc_TAS.variables['lat']
        lons = nc_TAS.variables['lon']
        mon_TAS = ma.masked_equal(liste_TAS[0], liste_TAS[0]._FillValue)[:,
                  lu.find_closest(lats[:], min_lats):lu.find_closest(lats[:], max_lats) + 1, :]
        plot_lats = lats[lu.find_closest(lats[:], min_lats):lu.find_closest(lats[:], max_lats) + 1]

    # ==========

    # ==========
    elif dataset == "subgrid":
        # ========== CRU_TS / VASClimO

        tas_File = "test-data/monthly_climatology.nc"
        prc_File = "test-data/monthly_climatology.nc"

        var_temp = "Tann"
        var_Grid = "Acc"

        liste_PRC, nc_PRC = lu.read_var_NC(prc_File, [var_Grid, ])  # returns a list, in
        mon_PRC = ma.masked_equal(liste_PRC[0], -99999.0) * 1000.

        # Convert europe coord data:
        # sed -e 's/ \+ /\t/g' europe-15min_coord.dat | sed -e 's/^\t//g' > europe-15min_coord-tabs.dat
        #
        data_array = lu.read_txt("test-data/europe-15min_coord-tabs.dat", cols=6)

        # ~ lats_PRC = nc_PRC.variables['y']

        # ~ max_lats = lats_PRC[-1]
        # ~ min_lats = lats_PRC[0]

        liste_TAS, nc_TAS = lu.read_var_NC(tas_File, [var_temp, ])  # returns a list, in  C

        # ~ lats = nc_TAS.variables['lat']
        # ~ lons = nc_TAS.variables['lon']

        lats = data_array[3, ::256]
        lons = data_array[2, :256]

        mon_TAS = ma.masked_less(liste_TAS[0],
                                 -100.0)  #  [:,lu.find_closest(lats[:],min_lats):lu.find_closest(lats[:],max_lats)+1,:]
        # ~ plot_lats = lats[lu.find_closest(lats[:],min_lats):lu.find_closest(lats[:],max_lats)+1]
        plot_lats = lats
    elif dataset == "AZ":

        # ~ tas_File = "test-data/AZ_datasets/pi_corr_tem_av-newtime-365_days-monmean.nc"
        # ~ prc_File = "test-data/AZ_datasets/pi_corr_prc_av-newtime-365_days-monmean.nc"
        
        
        # pi_raw has temperature variable == tem and not temp //  and lat/lon being latitude/longitude
        # ~ tas_File = "test-data/AZ_datasets/pi_raw_tem_av-newtime-365_days-monmean.nc"
        # ~ prc_File = "test-data/AZ_datasets/pi_raw_prc_av-newtime-365_days-monmean.nc"        
        
        
        # ~ tas_File = "test-data/AZ_datasets/6k_corr_tem_av-newtime-365_days-monmean.nc"
        # ~ prc_File = "test-data/AZ_datasets/6k_corr_prc_av-newtime-365_days-monmean.nc"

        # ~ var_temp = "temp"
        # ~ var_temp = "tem"
        # ~ var_Grid = 'prc'

        tas_File = "test-data/AZ_datasets/land_observations_down_tem_av-newtime-365_days-monmean.nc"
        prc_File = "test-data/AZ_datasets/land_observations_down_prc_av-newtime-365_days-monmean.nc"

        var_temp = "tas"
        var_Grid = 'pr'

        

        liste_TAS, nc_TAS = lu.read_var_NC(tas_File, [var_temp, ])  # returns a list, in C
        mon_TAS = ma.masked_equal(liste_TAS[0], liste_TAS[0]._FillValue)
        
        # ~ lats = nc_TAS.variables['latitude']
        # ~ lons = nc_TAS.variables['longitude']
        # ~ lats = nc_TAS.variables['lat']
        # ~ lons = nc_TAS.variables['lon']
        lats = nc_TAS.variables['y']
        lons = nc_TAS.variables['x']
        
        
        plot_lats = lats

        liste_PRC, nc_PRC = lu.read_var_NC(prc_File, [var_Grid, ])  # returns a list, in mm.month-1
        mon_PRC = ma.masked_equal(liste_PRC[0], liste_PRC[0]._FillValue) # use a dummy value, no missing value in that file ...

        # Anhelina's datasets ...
        

    # ==========

    # end if on dataset

    # Minimum Monthly mean temperature
    T_min = ma.min(mon_TAS, axis=0)

    # Maximum Monthly mean temperature
    T_max = ma.max(mon_TAS, axis=0)

    # Annual mean temperature
    T_ann = ma.mean(mon_TAS, axis=0)
    # Number of months above the 10°C threshold ...
    T_mon = ma.sum(ma.masked_greater_equal(mon_TAS, 10.0).mask, axis=0)  #  T_mon no longer contains Monthly Temp.

    # Precipitation of the dryest month
    P_min = ma.min(mon_PRC, axis=0)
    # Precipitation of the wettest month
    P_max = ma.max(mon_PRC, axis=0)
    # Annual sum of precipitation
    P_ann = ma.sum(mon_PRC, axis=0)

    P_dry = ma.sum(ma.masked_less_equal(mon_PRC, 60.0).mask, axis=0)  # Count number of dry months

    print(ma.max(mon_PRC), T_mon.shape, P_dry.shape)

    # lets define summer in northern hemisphere as 3->8 (april, september included)
    # lets find the index of the equator ...

    indx_equ = lu.find_closest(lats[:], 0.0)
    # indx_equ = 0
    P_smin = ma.zeros(mon_PRC[0, ...].shape)
    P_smax = ma.zeros(mon_PRC[0, ...].shape)
    P_ssum = ma.zeros(mon_PRC[0, ...].shape)
    P_wmin = ma.zeros(mon_PRC[0, ...].shape)
    P_wmax = ma.zeros(mon_PRC[0, ...].shape)
    P_wsum = ma.zeros(mon_PRC[0, ...].shape)

    if dataset == "ERA":

        P_smax, P_smin, P_ssum = get_maxminsum_Slice(mon_PRC, indx_l=3, indx_h=9)  # N_Summer
        P_wmax, P_wmin, P_wsum = get_maxminsum_Slice(mon_PRC, indx_l=-3, indx_h=3)  # N_Winter

        exchange_tabs(P_smax[indx_equ:, :],
                      P_wmax[indx_equ:, :])  # exchange data south of the equator to match definition of arrays
        exchange_tabs(P_smin[indx_equ:, :], P_wmin[indx_equ:, :])
        exchange_tabs(P_ssum[indx_equ:, :], P_wsum[indx_equ:, :])

    elif dataset == "CRU" or dataset == "subgrid":

        P_smax, P_smin, P_ssum = get_maxminsum_Slice(mon_PRC, indx_l=3, indx_h=9)  # N_Summer
        P_wmax, P_wmin, P_wsum = get_maxminsum_Slice(mon_PRC, indx_l=-3, indx_h=3)  # N_Winter

        exchange_tabs(P_smax[:indx_equ, :],
                      P_wmax[:indx_equ, :])  # exchange data south of the equator to match definition of arrays
        exchange_tabs(P_smin[:indx_equ, :], P_wmin[:indx_equ, :])
        exchange_tabs(P_ssum[:indx_equ, :], P_wsum[:indx_equ, :])

    elif dataset == "AZ" : #  only Europe 

        P_smax, P_smin, P_ssum = get_maxminsum_Slice(mon_PRC, indx_l=3, indx_h=9)  # N_Summer
        P_wmax, P_wmin, P_wsum = get_maxminsum_Slice(mon_PRC, indx_l=-3, indx_h=3)  # N_Winter
		    
    # end if
    

    # end if

    # ~ #  Other version that includes finding the 6 warmest month ...
    # ~ # T_smooth = lu.smoothD(mon_TAS,window_len=6,window='flat')
    # ~ # np.roll(T_smooth[:,12,12],6)-T_smooth[:,12,12] gives the maximum difference (D.Paillard) of the shifted 6 months
    # ~ # np.argmax(np.roll(T_smooth[:,12,12],6)-T_smooth[:,12,12]) gives summer/winter month (2 before, 3 after)

    # ~ T_smooth = lu.smoothD(mon_TAS,window_len=6,window='flat')

    # ~ # Then, start of summer should be something like:
    # ~ # ma.argmin(np.roll(T_smooth[:,i,j],6)-T_smooth[:,i,j])-2
    # ~ # And the end of the summer should be three months afterwards:
    # ~ # ma.argmin(np.roll(T_smooth[:,i,j],6)-T_smooth[:,i,j])+3

    # ~ # Rewriting this in  slicing indexes:

    # ~ summer = ma.argmin(np.roll(T_smooth[:,:,:],6,axis=0)-T_smooth[:,:,:],axis=0)
    # ~ sum_strt = summer-2
    # ~ sum_endd = summer+4

    # ~ summerMA = ma.masked_array(summer,mask=T_smooth[0,...].mask)

    # ~ var2plot = summerMA

    # ~ fig = plt.figure(figsize=(10,10))
    # ~ ax = plt.axes(projection=ccrs.PlateCarree())

    # ~ mesh = ax.pcolormesh(lons[:], plot_lats[:], var2plot, transform=ccrs.PlateCarree())
    # ~ plt.colorbar(mesh, orientation='horizontal', shrink=0.75)
    # ~ ax.gridlines()
    # ~ ax.coastlines()

    P_th = ma.zeros(mon_TAS[0, ...].shape)

    P_wpro = P_wsum / P_ann
    P_spro = P_ssum / P_ann

    var_1 = ma.where(P_wpro >= 2. / 3., 2. * T_ann, 0.0)
    var_2 = ma.where(P_spro >= 2. / 3., 2. * T_ann + 28.0, 0.0)

    P_th = ma.where((var_1 + var_2) <= 0.0, 2 * T_ann + 14.0, var_1 + var_2)

    KG_map = ma.zeros(P_th.shape, np.int)
    KG_map.mask = True  #  (T_max.mask+P_max.mask)


    match typ_classification:
        case "kottek":
           # ~ Colormap for KG in Kottek et al., 2007
           KG_dict, the_chosen_map = CKG.KG_cmap_2006()           
        case "peel":
           # ~ Colormap for KG in Peel et al., 2007
           KG_dict, the_chosen_map = CKG.KG_cmap_2007() 
        case "cannon":
           # ~ Colormap for KG in Cannon, 2012
           KG_dict, the_chosen_map = CKG.KG_cmap_2012()
        case "trewartha":
           # ~ Colormap for Trewartha in Belda, 2014
           KG_dict, the_chosen_map = CKG.KG_cmap_2014()
        case _:
           sys.exit('Unkown classification request')   
    #end match

    # ~ widgets = [PB.Bar('>'), ' ', PB.ETA(), ' ', PB.ReverseBar('<')]
    # ~ widgets = [PB.SimpleProgress()]
    # ~ widgets = ['Test: ', PB.Percentage(), ' ', PB.Bar(marker=PB.RotatingMarker()),' ', PB.ETA(), ' ', PB.FileTransferSpeed()]
    widgets = [PB.Percentage(), PB.Bar()]

    init_shape = T_min.shape

    Asize = T_min.size

    ARGS = ma.zeros((13, Asize))

    ARGS[0, :] = T_min.flatten()
    ARGS[1, :] = T_max.flatten()
    ARGS[2, :] = T_mon.flatten()
    ARGS[3, :] = T_ann.flatten()
    ARGS[4, :] = P_min.flatten()
    ARGS[5, :] = P_ann.flatten()
    ARGS[6, :] = P_smin.flatten()
    ARGS[7, :] = P_smax.flatten()
    ARGS[8, :] = P_wmin.flatten()
    ARGS[9, :] = P_wmax.flatten()
    ARGS[10, :] = P_th.flatten()
    ARGS[11, :] = P_wpro.flatten()
    ARGS[12, :] = P_dry.flatten()

    KG_MAP = KG_map.flatten()

    pbar = PB.ProgressBar(widgets=widgets, maxval=Asize).start()

    start_time = time.time()

    for i in range(Asize):
        if  not ARGS.mask[4,i] and not ARGS.mask[0,i] :
            match typ_classification:
                case "kottek":
                    # ~ Koeppen-Geiger in the Peel or Kottek versions
                    KG_MAP[i] = KG_dict[get_kg_classification(ARGS[:, i], vers=typ_classification)]
                case "peel":
                    # ~ Koeppen-Geiger in the Peel or Kottek versions
                    KG_MAP[i] = KG_dict[get_kg_classification(ARGS[:, i], vers=typ_classification)]
                case "cannon":			
                    # ~ Cannon verified -- 2022-02-17
                    KG_MAP[i] = KG_dict[get_kg_classification_Cannon(ARGS[:,i])]
                case "trewartha":
                    # ~ Trewartha verified -- 2022-02-17
                    KG_MAP[i] = KG_dict[get_kg_classification_Trewartha(ARGS[:, i])]
            #end match
        # endif
        pbar.update(i)
    # end for

    KG_map = KG_MAP.reshape(init_shape)

    pbar.finish()

    print("--- %s seconds ---" % (time.time() - start_time))

    var2plot = KG_map

    fig = plt.figure(figsize=(10, 10))
    ax = plt.axes(projection=ccrs.PlateCarree())
    varmin = np.min(np.array(list(KG_dict.values())))-0.5
    varmax = np.max(np.array(list(KG_dict.values())))+0.5
    
    mesh = ax.pcolormesh(lons[:], plot_lats[:], var2plot, cmap=the_chosen_map, transform=ccrs.PlateCarree(),vmin=varmin, vmax=varmax)
    # ~ mesh = ax.pcolormesh(lons[:], plot_lats[:], P_wpro , transform=ccrs.PlateCarree())
    cbar = plt.colorbar(mesh, orientation='horizontal', shrink=1.25)

    cbar.set_ticks(np.arange(len(KG_dict.values()))+1.0)
    cbar.set_ticklabels(KG_dict.keys(), fontsize=8, weight='bold')
		
    ax.gridlines()
    ax.coastlines()

    plt.show()
# endif on main

# The End of All Things (op. cit.)
