#-*- coding: utf-8 -*-
import numpy as np
import math
import misc_utils as mu

# parameters
Inertia = 0.0022 # aka. 'J' in kg/(m^2)
Damping = 0.001  # aka. 'B' in Nm/(rad/s)
Kv = 1700.       # aka. motor constant in RPM/V
L = 0.00312      # aka. Coil inductance in H
R = 0.8          # aka. Phase resistence in Ohm
VDC = 100.      # aka. Supply voltage
NbPoles = 14.    # NbPoles / 2 = Number of pole pairs (you count the permanent magnets on the rotor to get NbPoles)

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
    phase_thetae = mu.norm_angle((X[sv_theta] * (NbPoles / 2.)) + thetae_offset)

    bemf_constant = (Kv * math.pi)/30. # aka. ke in V/rad/s
    max_bemf = bemf_constant * X[sv_omega]

    bemf = 0.
    if 0. <= phase_thetae <= (math.pi * (1./6.)):
        bemf = (max_bemf / (math.pi * (1./6.))) * phase_thetae
    elif (math.pi/6.) < phase_thetae <= (math.pi * (5./6.)):
        bemf = max_bemf
    elif (math.pi * (5./6.)) < phase_thetae <= (math.pi * (7./6.)):
        bemf = -((max_bemf/(math.pi/6.))* (phase_thetae - math.pi))
    elif (math.pi * (7./6.)) < phase_thetae <= (math.pi * (11./6.)):
        bemf = -max_bemf
    elif (math.pi * (11./6.)) < phase_thetae <= (2.0 * math.pi):
        bemf = (max_bemf/(math.pi/6.)) * (phase_thetae - (2. * math.pi))
    else:
        print "ERROR: angle out of bounds can not calculate bemf {}".format(phase_thetae)

    return bemf

#
# Dynamic model
#
# X state, t time, U input, W perturbation
#
def dyn(X, t, U, W):

    eu = backemf(X, 0.)
    ev = backemf(X, math.pi * (2./3.))
    ew = backemf(X, math.pi * (4./3.))

    # Electromagnetic torque
    etorque = (eu * X[sv_iu] + ev * X[sv_iv] + ew * X[sv_iw])/X[sv_omega]

    # Acceleration of the rotor
    omega_dot = ((etorque * (NbPoles / 2)) - (Damping * X[sv_omega]) - W[pv_torque]) / Inertia

    # Initialize the imposed
    vui = 0.
    vvi = 0.
    vwi = 0.

    # Phase voltages
    if U[iv_hu] == 1:
        vui = VDC/2.
    if U[iv_lu] == 1:
        vui = -VDC/2.
    if U[iv_hv] == 1:
        vvi = VDC/2.
    if U[iv_lv] == 1:
        vvi = -VDC/2.
    if U[iv_hw] == 1:
        vwi = VDC/2.
    if U[iv_lw] == 1:
        vwi = -VDC/2.

    # Mean voltage in the motor, assuming star configuration
    vtotal = ((vui + vvi + vwi) - (eu + ev + ew))
    vm = 0.

    if X[sv_iu] == 0:   # phase V & W are conducting current
        vm = vtotal / 2.
        vu = eu
        vv = vvi - vm
        vw = vwi - vm
    elif X[sv_iv] == 0: # phase U & W are conducting current
        vm = vtotal / 2.
        vu = vui - vm
        vv = ev
        vw = vwi - vm
    elif X[sv_iw] == 0: # phase U & V are conducting current
        vm = vtotal / 2.
        vu = vui - vm
        vv = vvi - vm
        vw = ew
    else:               # all phases are corducting current
        vm = vtotal / 3.
        vu = vui - vm
        vv = vvi - vm
        vw = vwi - vm

    iu_dot = (1./L) * (vu - (R * X[sv_iu]) - eu - vm)
    iv_dot = (1./L) * (vv - (R * X[sv_iv]) - ev - vm)
    iw_dot = (1./L) * (vw - (R * X[sv_iw]) - ew - vm)

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
