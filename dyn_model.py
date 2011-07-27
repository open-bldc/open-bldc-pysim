#-*- coding: utf-8 -*-
import numpy as np

# parameters
Inertia = 1    # aka. 'J'
Damping = 0.25 # aka. 'B'
Kv = 1700      # aka. RPM/V
L = 3          # aka. Coil inductance in H
R = 0.02       # aka. Phase resistence in Ohm
VDC = 100      # aka. Supply voltage

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
pv_trorque  = 0
pv_size = 1

# Calculate backemf at a given omega offset from the current rotor position
#
# Used to calculate the phase backemf aka. 'e'
#
def backemf(X,omega_offset):
    omega = X[sv_omega] + omega_offset
    bemf_constant = (MotorKv * mat.pi)/30 # aka. ke in V/rad/s
    max_bemf = bemf_constant * X[sv_omega]

    if (omega > 0) && (omega <= (mat.pi/6)):
        bemf = (max_bemf / (mat.pi/6)) * omega
    elif (omega > (mat.pi/6)) && (omega <= (mat.pi * (5/6))):
        bemf = max_bemf
    elif (omega > (mat.pi * (5/6))) && (omega <= (mat.pi * (7/6))):
        bemf = -((max_bemf/(mat.pi/6))* (omega - mat.pi))
    elif (omega > (mat.pi * (7/6))) && (omega <= (mat.pi * (11/6))):
        bemf = -max_bemf
    elif (omega > (mat.pi * (11/6))) && (omega <= (2 * mat.pi)):
        bemf = (max_bemf/(mat.pi/6)) * (omega - (2 * mat.pi))

    return bemf

#
# Dynamic model
#
# X state, t time, U input, W perturbation
#
def dyn(X, t, U, W):

    eu = backemf(X, 0)
    ev = backemf(X, mat.pi * (2/3))
    ew = backemf(X, mat.pi * (4/3))

    # Electromagnetic torque
    torque = (eu * X[sv_iu] + ev * X[sv_iv] + ew * X[sv_iw])/X[sv_omega]

    # Acceleration of the rotor
    omega_dot = 1/Inertia * (torque - Damping * X[sv_omega] - W[torque])

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
    vm = 

    iu_dot = (1/Inductance) * (vu - (R * X[sv_iu]) - eu - vm)
    iv_dot = (1/Inductance) * (vv - (R * X[sv_iv]) - ev - vm)
    iw_dot = (1/Inductance) * (vw - (R * X[sv_iw]) - ew - vm)

    Xd = [  X[sv_omega],
            ]
    return Xd
