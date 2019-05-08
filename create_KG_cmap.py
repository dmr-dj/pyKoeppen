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

    # Color scheme used by Kottek et al., 2006

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


    return KG_dict, mpl.colors.ListedColormap(List_Colors)
#end def KG_cmap_2006

def KG_cmap_2007() :
    import matplotlib as mpl

    # Color scheme used by Peel et al., 2007

    # Hex colors
    # Af    010feb
    # Am    0e72f9
    # As    ??????	Does not exist in Peel et al., 2007
    # Aw    42a8fd
    # BWk   f29790
    # BWh   f60000
    # BSk   ffda65
    # BSh   f2a406
    # Cfa   cbf74c
    # Cfb   66ec2e
    # Cfc   4bca23
    # Csa   f3fa00
    # Csb   c7c804
    # Csc   ??????	Does not occur in Peel et al., 2007 || Proposed: a7a900
    # Cwa   98d995
    # Cwb   65ca5e
    # Cwc   399a36
    # Dfa   15fffe
    # Dfb   39c7f8
    # Dfc   04767c
    # Dfd   0b4560
    # Dsa   f500fe
    # Dsb   de00c7
    # Dsc   932e95
    # Dsd   956492
    # Dwa   adacd5
    # Dwb   597bda
    # Dwc   5054b0
    # Dwd   2b0d7c
    # EF    65696c
    # ET    b3afb0

    List_Colors = ['#010feb','#0e72f9','#42a8fd','#f29790','#f60000','#ffda65','#f2a406',
                   '#cbf74c','#66ec2e','#4bca23','#f3fa00','#c7c804','#a7a900','#98d995',
                   '#65ca5e','#399a36','#15fffe','#39c7f8','#04767c','#0b4560','#f500fe',
                   '#de00c7','#932e95','#956492','#adacd5','#597bda','#5054b0','#2b0d7c','#65696c',
                   '#b3afb0']


    KG_dict = {
              "Af"  :  1,
              "Am"  :  2,
              "Aw"  :  3,
              "BWk" :  4,
              "BWh" :  5,
              "BSk" :  6,
              "BSh" :  7,
              "Cfa" :  8,
              "Cfb" :  9,
              "Cfc" : 10,
              "Csa" : 11,
              "Csb" : 12,
              "Csc" : 13,
              "Cwa" : 14,
              "Cwb" : 15,
              "Cwc" : 16,
              "Dfa" : 17,
              "Dfb" : 18,
              "Dfc" : 19,
              "Dfd" : 20,
              "Dsa" : 21,
              "Dsb" : 22,
              "Dsc" : 23,
              "Dsd" : 24,
              "Dwa" : 25,
              "Dwb" : 26,
              "Dwc" : 27,
              "Dwd" : 28,
              "EF"  : 29,
              "ET"  : 30
              }

    return KG_dict, mpl.colors.ListedColormap(List_Colors)
#end def KG_cmap_2006



# The End of All Things (op. cit.)
