#-*- coding: utf-8 -*-
import numpy as np
import math
import misc_utils as mu

# parameters
if 0:
    Inertia = 0.0022 # aka. 'J' in kg/(m^2)
    Damping = 0.001  # aka. 'B' in Nm/(rad/s)
    Kv = 1700.       # aka. motor constant in RPM/V
    L = 0.00312      # aka. Coil inductance in H
    R = 0.8          # aka. Phase resistence in Ohm
    VDC = 100.       # aka. Supply voltage
    NbPoles = 14.    # NbPoles / 2 = Number of pole pairs (you count the permanent magnets on the rotor to get NbPoles)
else: #psim
    Inertia = 0.000006            # aka. 'J' in kg/(m^2)
    tau_shaft = 0.006
    Damping = Inertia/tau_shaft   # aka. 'B' in Nm/(rad/s)
    Kv = 1./32.3*1000             # aka. motor constant in RPM/V
    L = 0.00207                   # aka. Coil inductance in H
    R = 11.9                      # aka. Phase resistence in Ohm
    VDC = 300.                    # aka. Supply voltage
    NbPoles = 4.                  # 
    
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
ov_iu      = 0
ov_iv      = 1
ov_iw      = 2
ov_vu      = 3
ov_vv      = 4
ov_vw      = 5
ov_omega   = 6
ov_theta   = 7
ov_size    = 8

# Phases and star vector designators
ph_U = 0
ph_V = 1
ph_W = 2
ph_star = 3
ph_size = 4

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
# Calculate phase voltages
# Returns a vector of phase voltages in reference to the star point
def voltages(X, U):

    eu = backemf(X, 0.)
    ev = backemf(X, math.pi * (2./3.))
    ew = backemf(X, math.pi * (4./3.))

    # Initialize the imposed terminal voltages
    vui = 0.
    vvi = 0.
    vwi = 0.

    # Phase input voltages based on the inverter switches states
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

    V = [ vu,
          vv,
          vw,
          vm
          ]

    return V

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

    V = voltages(X, U)

    iu_dot = (1./L) * (V[ph_U] - (R * X[sv_iu]) - eu - V[ph_star])
    iv_dot = (1./L) * (V[ph_V] - (R * X[sv_iv]) - ev - V[ph_star])
    iw_dot = (1./L) * (V[ph_W] - (R * X[sv_iw]) - ew - V[ph_star])

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
def output(X, U):

    V = voltages(X, U)

    Y = [X[sv_iu], X[sv_iv], X[sv_iw],
         V[ph_U], V[ph_V], V[ph_W],
         X[sv_omega], X[sv_theta]]

    return Y
