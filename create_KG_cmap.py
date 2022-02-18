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
#end def KG_cmap_2007

def KG_cmap_2012() :
    import matplotlib as mpl

    # Color scheme used by Cannon, 2012

    # Hex colors
    # 1WW   fd0001
    # 1WD   fe5400
    # 1DW   fcaa00
    # 1DD   fefe00
    # 2Ww   8fed8f
    # 2Wd   72d374
    # 2Dh   54b554

    # 2Dc   3a9b3a
    # 2Dw   1c7d1c
    # 2Dd   006301
    # 3hh   890101
    # 3hW   941818
    # 3hD   9b3332
    # 3cw   a4504e

    # 3cd   b0686b
    # 3Hw   b78481
    # 3Hd   be9f9d
    # 3CH   cbb7b8
    # 3CC   d2d2d2
    # 4Ww   fc69b0
    # 4Wd   eb59be

    # 4HW   db4acd
    # 4HD   c53ed8
    # 4Ch   b32de2
    # 4Cc   9f20ed
    # 5hh   010088
    # 5hc   003fa7
    # 5hC   017ec1
    # 5cw   02bee3

    # 5cd   00fefc


    List_Colors = ['#fd0001','#fe5400','#fcaa00','#fefe00','#8fed8f','#72d374','#54b554',
                   '#3a9b3a','#1c7d1c','#006301','#890101','#941818','#9b3332','#a4504e',
                   '#b0686b','#b78481','#be9f9d','#cbb7b8','#d2d2d2','#fc69b0','#eb59be',
                   '#db4acd','#c53ed8','#b32de2','#9f20ed','#010088','#003fa7','#017ec1','#02bee3',
                   '#00fefc']

    KG_dict = {
              "1WW" :  1,
              "1WD" :  2,
              "1DW" :  3,
              "1DD" :  4,
              "2Ww" :  5,
              "2Wd" :  6,
              "2Dh" :  7,
              "2Dc" :  8,
              "2Dw" :  9,
              "2Dd" : 10,
              "3hh" : 11,
              "3hW" : 12,
              "3hD" : 13,
              "3cw" : 14,
              "3cd" : 15,
              "3Hw" : 16,
              "3Hd" : 17,
              "3CH" : 18,
              "3CC" : 19,
              "4Ww" : 20,
              "4Wd" : 21,
              "4HW" : 22,
              "4HD" : 23,
              "4Ch" : 24,
              "4Cc" : 25,
              "5hh" : 26,
              "5hc" : 27,
              "5hC" : 28,
              "5cw" : 29,
              "5cd" : 30
              }

    return KG_dict, mpl.colors.ListedColormap(List_Colors)
#end def KG_cmap_2012

def KG_cmap_2014() :
    import matplotlib as mpl

    # Color scheme used by Belda et al., 2014

    # Hex colors
    # Ar    84070b
    # Aw    cd1c0a
    # As    b64f04
    # BW    ffde49
    # BS    f09137
    # Cs    9fc301
    # Cw    2c8a29
    # Cf    009736
    # Do    00add7
    # Dc    b2559c
    # Eo    1451a1
    # Ec    0c356b
    # Ft    c0c0c0
    # Fi    8c8c8c

    List_Colors = ['#84070b','#cd1c0a','#b64f04','#ffde49','#f09137','#9fc301','#2c8a29','#009736',
                   '#00add7','#b2559c','#1451a1','#0c356b','#c0c0c0','#8c8c8c']

    KG_dict = {
              "Ar"  :  1,
              "Aw"  :  2,
              "As"  :  3,
              "BW"  :  4,
              "BS"  :  5,
              "Cs"  :  6,
              "Cw"  :  7,
              "Cr"  :  8,
              "Do"  :  9,
              "Dc"  : 10,
              "Eo"  : 11,
              "Ec"  : 12,
              "Ft"  : 13,
              "Fi"  : 14
              }


    return KG_dict, mpl.colors.ListedColormap(List_Colors, name="belda14", N=14)
#end def KG_cmap_2006
# The End of All Things (op. cit.)
