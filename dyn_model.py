#-*- coding: utf-8 -*-
import numpy as np
import math
import misc_utils as mu

# parameters
Inertia = 1    # aka. 'J'
Damping = 0.25 # aka. 'B'
Kv = 1700      # aka. RPM/V
L = 3          # aka. Coil inductance in H
R = 0.02       # aka. Phase resistence in Ohm
VDC = 100      # aka. Supply voltage
NbPoles = 14   # NbPoles / 2 = Number of pole pairs (you count the permanent magnets on the rotor to get NbPoles)

# Components of the state vector
sv_theta  = 0      # angle of the rotor
sv_omega = 1       # angular speed of the rotor
sv_iu = 2          # phase u current
sv_iv = 3          # phase v current
sv_iw = 4          # phase w current
sv_size = 5


# Components of the command vector
iv_lu   = 0
iv_hu   = 1
iv_lv   = 2
iv_hv   = 3
iv_lw   = 4
iv_hw   = 5
iv_size = 6


# Components of the perturbation vector
pv_torque  = 0
pv_size = 1

# Components of the output vector
ov_comp_uv = 0
ov_comp_vw = 1
ov_comp_uw = 2
ov_theta   = 3
ov_size    = 4


#
# Calculate backemf at a given omega offset from the current rotor position
#
# Used to calculate the phase backemf aka. 'e'
#
def backemf(X,thetae_offset):
    thetae = mu.norm_angle(X[sv_theta] * (NbPoles / 2))
    phase_thetae = thetae + thetae_offset
    bemf_constant = (Kv * math.pi)/30 # aka. ke in V/rad/s
    max_bemf = bemf_constant * X[sv_omega]
    bemf = 0
    if (thetae > 0) and (thetae <= (math.pi/6)):
        bemf = (max_bemf / (math.pi/6)) * thetae
    elif (thetae > (math.pi/6)) and (thetae <= (math.pi * (5/6))):
        bemf = max_bemf
    elif (thetae > (math.pi * (5/6))) and (thetae <= (math.pi * (7/6))):
        bemf = -((max_bemf/(math.pi/6))* (thetae - math.pi))
    elif (thetae > (math.pi * (7/6))) and (thetae <= (math.pi * (11/6))):
        bemf = -max_bemf
    elif (thetae > (math.pi * (11/6))) and (thetae <= (2 * math.pi)):
        bemf = (max_bemf/(math.pi/6)) * (thetae - (2 * math.pi))

    return bemf

#
# Dynamic model
#
# X state, t time, U input, W perturbation
#
def dyn(X, t, U, W):

    eu = backemf(X, 0)
    ev = backemf(X, math.pi * (2/3))
    ew = backemf(X, math.pi * (4/3))

    # Electromagnetic torque
    torque = (eu * X[sv_iu] + ev * X[sv_iv] + ew * X[sv_iw])/X[sv_omega]

    # Acceleration of the rotor
    omega_dot = 1/Inertia * (torque - Damping * X[sv_omega] - W[pv_torque])

    # Initialize the imposed
    vui = 0
    vvi = 0
    vwi = 0

    # Phase voltages
    if U[iv_hu]:
        vui = VDC/2
    if U[iv_lu]:
        vui = -VDC/2
    if U[iv_hv]:
        vvi = VDC/2
    if U[iv_lv]:
        vvi = -VDC/2
    if U[iv_hw]:
        vwi = VDC/2
    if U[iv_lw]:
        vwi = -VDC/2

    # Mean voltage in the motor, assuming star configuration
    vm = 0

    iu_dot = (1/L) * (vui - (R * X[sv_iu]) - eu - vm)
    iv_dot = (1/L) * (vvi - (R * X[sv_iv]) - ev - vm)
    iw_dot = (1/L) * (vwi - (R * X[sv_iw]) - ew - vm)

    Xd = [  X[sv_omega],
            omega_dot,
            iu_dot,
            iv_dot,
            iw_dot
        ]

    return Xd


#
#
#
def output(X):

    Y = [0, 0, 0, X[sv_theta]]
    return Y
