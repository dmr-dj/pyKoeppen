# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 18:10:07 CET 2019
Last modified, Fri Jan 18 18:10:07 CET 2019

@author: Didier M. Roche a.k.a. dmr
"""

# Changes from version 0.1 :

__version__ = "0.1"


def KG_cmap_2006() :
    import matplotlib as mpl


    # Hex colors
    # Af    960000
    # Am    ff0000
    # As    ff9999
    # Aw    ffcccc  ##
    # BWk   ffff64
    # BWh   ffcc00
    # BSk   ccaa54
    # BSh   cc8d14
    # Cfa   003200
    # Cfb   005000
    # Cfc   007800
    # Csa   00ff00
    # Csb   96ff00
    # Csc   c8ff00
    # Cwa   b46400
    # Cwb   966400
    # Cwc   5a3c00
    # Dfa   320032
    # Dfb   640064
    # Dfc   c800c8
    # Dfd   c71585
    # Dsa   ff6dff
    # Dsb   ffb4ff
    # Dsc   e6c8ff
    # Dsd   c8c8c8
    # Dwa   c8b4ff
    # Dwb   9a7fb3
    # Dwc   8859b3
    # Dwd   6f24b3 ##
    # EF    6496ff
    # ET    64ffff

    List_Colors = ['#960000','#ff0000','#ff9999','#ffcccc','#ffff64','#ffcc00','#ccaa54','#cc8d14',
                   '#003200','#005000','#007800','#00ff00','#96ff00','#c8ff00','#b46400',
                   '#966400','#5a3c00','#320032','#640064','#c800c8','#c71585','#ff6dff',
                   '#ffb4ff','#e6c8ff','#c8c8c8','#c8b4ff','#9a7fb3','#8859b3','#6f24b3','#6496ff',
                   '#64ffff']
    return mpl.colors.ListedColormap(List_Colors)
#end def KG_cmap_2006

# The End of All Things (op. cit.)
