# -*- coding: utf-8 -*-
#
# Open-BLDC pysim - Open BrushLess DC Motor Controller python simulator
# Copyright (C) 2011 by Antoine Drouin <poinix@gmail.com>
# Copyright (C) 2011 by Piotr Esden-Tempski <piotr@esden.net>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import numpy as np
import math
import misc_utils as mu

# parameters
pset = 2

if pset == 0:
    Inertia = 0.0022  # aka. 'J' in kg/(m^2)
    Damping = 0.001  # aka. 'B' in Nm/(rad/s)
    Kv = 1700.0  # aka. motor constant in RPM/V
    L = 0.00312  # aka. Coil inductance in H
    M = 0.0  # aka. Mutual inductance in H
    R = 0.8  # aka. Phase resistence in Ohm
    VDC = 100.0  # aka. Supply voltage
    NbPoles = 14.0  # NbPoles / 2 = Number of pole pairs (you count the permanent magnets on the rotor to get NbPoles)
    dvf = 0.7  # aka. freewheeling diode forward voltage
elif pset == 1:
    Inertia = 0.0022  # aka. 'J' in kg/(m^2)
    Damping = 0.001  # aka. 'B' in Nm/(rad/s)
    Kv = 70.0  # aka. motor constant in RPM/V
    L = 0.00521  # aka. Coil inductance in H
    M = 0.0  # aka. Mutual inductance in H
    R = 0.7  # aka. Phase resistence in Ohm
    VDC = 100.0  # aka. Supply voltage
    NbPoles = 4.0  # NbPoles / 2 = Number of pole pairs (you count the permanent magnets on the rotor to get NbPoles)
    dvf = 0.7  # aka. freewheeling diode forward voltage
elif pset == 2:  # psim
    Inertia = 0.000007  # aka. 'J' in kg/(m^2)
    tau_shaft = 0.006
    Damping = Inertia / tau_shaft  # aka. 'B' in Nm/(rad/s)
    Kv = 1.0 / 32.3 * 1000  # aka. motor constant in RPM/V
    L = 0.00207  # aka. Coil inductance in H
    M = -0.00069  # aka. Mutual inductance in H
    R = 11.9  # aka. Phase resistence in Ohm
    VDC = 100.0  # aka. Supply voltage
    NbPoles = 4.0  #
    dvf = 0.0  # aka. freewheeling diode forward voltage
elif pset == 3:  # modified psim
    Inertia = 0.000059  # aka. 'J' in kg/(m^2)
    tau_shaft = 0.006
    Damping = Inertia / tau_shaft  # aka. 'B' in Nm/(rad/s)
    Kv = 1.0 / 32.3 * 1000  # aka. motor constant in RPM/V
    L = 0.00207  # aka. Coil inductance in H
    M = -0.00069  # aka. Mutual inductance in H
    R = 11.9  # aka. Phase resistence in Ohm
    VDC = 300.0  # aka. Supply voltage
    NbPoles = 4.0  #
    dvf = 0.0  # aka. freewheeling diode forward voltage
else:
    print("Unknown pset {}".format(pset))

# Components of the state vector
sv_theta = 0  # angle of the rotor
sv_omega = 1  # angular speed of the rotor
sv_iu = 2  # phase u current
sv_iv = 3  # phase v current
sv_iw = 4  # phase w current
sv_size = 5


# Components of the command vector
iv_lu = 0
iv_hu = 1
iv_lv = 2
iv_hv = 3
iv_lw = 4
iv_hw = 5
iv_size = 6


# Components of the perturbation vector
pv_torque = 0
pv_friction = 1
pv_size = 2

# Components of the output vector
ov_iu = 0
ov_iv = 1
ov_iw = 2
ov_vu = 3
ov_vv = 4
ov_vw = 5
ov_theta = 6
ov_omega = 7
ov_size = 8

# Phases and star vector designators
ph_U = 0
ph_V = 1
ph_W = 2
ph_star = 3
ph_size = 4

# Debug vector components
dv_eu = 0
dv_ev = 1
dv_ew = 2
dv_ph_U = 3
dv_ph_V = 4
dv_ph_W = 5
dv_ph_star = 6
dv_size = 7


#
# Calculate backemf at a given omega offset from the current rotor position
#
# Used to calculate the phase backemf aka. 'e'
#
def backemf(X, thetae_offset):
    phase_thetae = mu.norm_angle((X[sv_theta] * (NbPoles / 2.0)) + thetae_offset)

    bemf_constant = mu.vpradps_of_rpmpv(Kv)  # aka. ke in V/rad/s
    max_bemf = bemf_constant * X[sv_omega]

    bemf = 0.0
    if 0.0 <= phase_thetae <= (math.pi * (1.0 / 6.0)):
        bemf = (max_bemf / (math.pi * (1.0 / 6.0))) * phase_thetae
    elif (math.pi / 6.0) < phase_thetae <= (math.pi * (5.0 / 6.0)):
        bemf = max_bemf
    elif (math.pi * (5.0 / 6.0)) < phase_thetae <= (math.pi * (7.0 / 6.0)):
        bemf = -((max_bemf / (math.pi / 6.0)) * (phase_thetae - math.pi))
    elif (math.pi * (7.0 / 6.0)) < phase_thetae <= (math.pi * (11.0 / 6.0)):
        bemf = -max_bemf
    elif (math.pi * (11.0 / 6.0)) < phase_thetae <= (2.0 * math.pi):
        bemf = (max_bemf / (math.pi / 6.0)) * (phase_thetae - (2.0 * math.pi))
    else:
        print(
            "ERROR: angle out of bounds can not calculate bemf {}".format(phase_thetae)
        )

    return bemf


#
# Calculate phase voltages
# Returns a vector of phase voltages in reference to the star point
def voltages(X, U):
    eu = backemf(X, 0.0)
    ev = backemf(X, math.pi * (2.0 / 3.0))
    ew = backemf(X, math.pi * (4.0 / 3.0))

    # Check which phases are excited
    pux = (U[iv_hu] == 1) or (U[iv_lu] == 1)

    pvx = (U[iv_hv] == 1) or (U[iv_lv] == 1)

    pwx = (U[iv_hw] == 1) or (U[iv_lw] == 1)

    vu = 0.0
    vv = 0.0
    vw = 0.0
    vm = 0.0

    if pux and pvx and pwx:
        if U[iv_hu] == 1:
            vu = VDC / 2.0
        else:
            vu = -VDC / 2.0

        if U[iv_hv] == 1:
            vv = VDC / 2.0
        else:
            vv = -VDC / 2.0

        if U[iv_hw] == 1:
            vw = VDC / 2.0
        else:
            vw = -VDC / 2.0

        vm = (vu + vv + vw - eu - ev - ew) / 3.0

    elif pux and pvx:
        # calculate excited phase voltages
        if U[iv_hu] == 1:
            vu = VDC / 2.0
        else:
            vu = -VDC / 2.0

        if U[iv_hv] == 1:
            vv = VDC / 2.0
        else:
            vv = -VDC / 2.0

        # calculate star voltage
        vm = (vu + vv - eu - ev) / 2.0

        # calculate remaining phase voltage
        vw = ew + vm

        # clip the voltage to freewheeling diodes
        # if (vw > ((VDC/2) + dvf)):
        #    vw = (VDC/2) + dvf;
        #    vm = (vu + vv + vw - eu - ev - ew) / 3.
        # elif (vw < (-(VDC/2) - dvf)):
        #    vw = -(VDC/2) - dvf;
        #    vm = (vu + vv + vw - eu - ev - ew) / 3.

    elif pux and pwx:
        if U[iv_hu] == 1:
            vu = VDC / 2.0
        else:
            vu = -VDC / 2.0

        if U[iv_hw] == 1:
            vw = VDC / 2.0
        else:
            vw = -VDC / 2.0

        vm = (vu + vw - eu - ew) / 2.0
        vv = ev + vm

        # clip the voltage to freewheeling diodes
        # if (vv > ((VDC/2) + dvf)):
        #    vv = (VDC/2) + dvf;
        #    vm = (vu + vv + vw - eu - ev - ew) / 3.
        # elif (vv < (-(VDC/2) - dvf)):
        #    vv = -(VDC/2) - dvf;
        #    vm = (vu + vv + vw - eu - ev - ew) / 3.

    elif pvx and pwx:
        if U[iv_hv] == 1:
            vv = VDC / 2.0
        else:
            vv = -VDC / 2.0

        if U[iv_hw] == 1:
            vw = VDC / 2.0
        else:
            vw = -VDC / 2.0

        vm = (vv + vw - ev - ew) / 2.0
        vu = eu + vm

        # clip the voltage to freewheeling diodes
        # if (vu > ((VDC/2) + dvf)):
        #    vu = (VDC/2) + dvf;
        #    vm = (vu + vv + vw - eu - ev - ew) / 3.
        # elif (vu < (-(VDC/2) - dvf)):
        #    vu = -(VDC/2) - dvf;
        #    vm = (vu + vv + vw - eu - ev - ew) / 3.

    elif pux:
        if U[iv_hu] == 1:
            vu = VDC / 2
        else:
            vu = -VDC / 2.0

        vm = vu - eu
        vv = ev + vm
        vw = ew + vm

    # if we want to handle diodes properly how to do that here?

    elif pvx:
        if U[iv_hv] == 1:
            vv = VDC / 2
        else:
            vv = -VDC / 2.0

        vm = vv - ev
        vu = eu + vm
        vw = ew + vm
    elif pwx:
        if U[iv_hw] == 1:
            vw = VDC / 2
        else:
            vw = -VDC / 2.0

        vm = vw - ew
        vu = eu + vm
        vv = ev + vm
    else:
        vm = eu
        vv = ev
        vw = ew

    #    # Initialize the imposed terminal voltages
    #    vui = 0.
    #    vvi = 0.
    #    vwi = 0.
    #
    #    # Phase input voltages based on the inverter switches states
    #    if (U[iv_hu] == 1) or (U[iv_dhu] == 1):
    #        vui = VDC/2.
    #    if (U[iv_lu] == 1) or (U[iv_dlu] == 1):
    #        vui = -VDC/2.
    #    if (U[iv_hv] == 1) or (U[iv_dhv] == 1):
    #        vvi = VDC/2.
    #    if (U[iv_lv] == 1) or (U[iv_dlv] == 1):
    #        vvi = -VDC/2.
    #    if (U[iv_hw] == 1) or (U[iv_dhw] == 1):
    #        vwi = VDC/2.
    #    if (U[iv_lw] == 1) or (U[iv_dlw] == 1):
    #        vwi = -VDC/2.
    #
    #    #i_thr = 0.001 # current threshold saying that the phase is not conducting
    #    i_thr = 0. # current threshold saying that the phase is not conducting
    #    #if -i_thr < X[sv_iu] < i_thr:   # phase V & W are conducting current
    #    if not pux:   # phase V & W are conducting current
    #        vm = ((vvi + vwi) / 2.) - ((ev + ew) / 2.)
    #        vu = eu
    #        vv = vvi - vm
    #        vw = vwi - vm
    #    elif not pvx: # phase U & W are conducting current
    #        vm = ((vui + vwi) / 2.) - ((eu + ew) / 2.)
    #        vu = vui - vm
    #        vv = ev
    #        vw = vwi - vm
    #    elif not pwx: # phase U & V are conducting current
    #        vm = ((vui + vvi) / 2.) - ((eu + ev) / 2.)
    #        vu = vui - vm
    #        vv = vvi - vm
    #        vw = ew
    #    else:               # all phases are corducting current
    #        print "all phases are conducting!"
    #        vm = ((vui + vvi + vwi) / 3.) - ((eu + ev + ew) / 3.)
    #        vu = vui - vm
    #        vv = vvi - vm
    #        vw = vwi - vm

    #    print "{} : {} {} {}".format(X[sv_omega], vu, vv, vw )

    V = [vu, vv, vw, vm]

    return V


#
# Dynamic model
#
# X state, t time, U input, W perturbation
#
def dyn(X, t, U, W):
    Xd, Xdebug = dyn_debug(X, t, U, W)

    return Xd


# Dynamic model with debug vector
def dyn_debug(X, t, U, W):
    eu = backemf(X, 0.0)
    ev = backemf(X, math.pi * (2.0 / 3.0))
    ew = backemf(X, math.pi * (4.0 / 3.0))

    # Electromagnetic torque
    etorque = (eu * X[sv_iu] + ev * X[sv_iv] + ew * X[sv_iw]) / X[sv_omega]

    # Mechanical torque
    mtorque = (etorque * (NbPoles / 2)) - (Damping * X[sv_omega]) - W[pv_torque]

    if (mtorque > 0) and (mtorque <= W[pv_friction]):
        mtorque = 0
    elif mtorque >= W[pv_friction]:
        mtorque = mtorque - W[pv_friction]
    elif (mtorque < 0) and (mtorque >= (-W[pv_friction])):
        mtorque = 0
    elif mtorque <= (-W[pv_friction]):
        mtorque = mtorque + W[pv_friction]

    # Acceleration of the rotor
    omega_dot = mtorque / Inertia

    V = voltages(X, U)

    pdt = VDC / 2 + dvf

    iu_dot = (V[ph_U] - (R * X[sv_iu]) - eu - V[ph_star]) / (L - M)
    iv_dot = (V[ph_V] - (R * X[sv_iv]) - ev - V[ph_star]) / (L - M)
    iw_dot = (V[ph_W] - (R * X[sv_iw]) - ew - V[ph_star]) / (L - M)

    Xd = [X[sv_omega], omega_dot, iu_dot, iv_dot, iw_dot]

    Xdebug = [eu, ev, ew, V[ph_U], V[ph_V], V[ph_W], V[ph_star]]

    return Xd, Xdebug


#
#
#
def output(X, U):
    V = voltages(X, U)

    Y = [
        X[sv_iu],
        X[sv_iv],
        X[sv_iw],
        V[ph_U],
        V[ph_V],
        V[ph_W],
        X[sv_theta],
        X[sv_omega],
    ]

    return Y
