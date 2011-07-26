#-*- coding: utf-8 -*-
import numpy as np

# parameters
Inertia = 1    #
Drag    = 0.25  #

# Components of the state vector
sv_alpha  = 0
sv_alphad = 1
sv_size   = 2


# Components of the command vector
iv_lu   = 0
iv_hu   = 1
iv_lv   = 2
iv_hv   = 3
iv_lw   = 4
iv_hw   = 5
iv_size = 6


# Components of the perturbation vector
pv_trq  = 0
pv_size = 1


#
# Dynamic model
#
# X state, t time, U input, W perturbation
#
def dyn(X, t, U, W):

    Xd = [  X[sv_alphad],
           -Drag/Inertia*X[sv_alphad]**2
            ]
    return Xd
