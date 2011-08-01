#-*- coding: utf-8 -*-
import numpy as np
import math
import misc_utils as mu

# parameters
pset = 3

if pset == 0:
    Inertia = 0.0022 # aka. 'J' in kg/(m^2)
    Damping = 0.001  # aka. 'B' in Nm/(rad/s)
    Kv = 1700.       # aka. motor constant in RPM/V
    L = 0.00312      # aka. Coil inductance in H
    M = 0.0          # aka. Mutual inductance in H
    R = 0.8          # aka. Phase resistence in Ohm
    VDC = 100.       # aka. Supply voltage
    NbPoles = 14.    # NbPoles / 2 = Number of pole pairs (you count the permanent magnets on the rotor to get NbPoles)
    dvf = .7         # aka. freewheeling diode forward voltage
elif pset == 1:
    Inertia = 0.0022 # aka. 'J' in kg/(m^2)
    Damping = 0.001  # aka. 'B' in Nm/(rad/s)
    Kv = 70.         # aka. motor constant in RPM/V
    L = 0.00521      # aka. Coil inductance in H
    M = 0.0          # aka. Mutual inductance in H
    R = 0.7          # aka. Phase resistence in Ohm
    VDC = 100.       # aka. Supply voltage
    NbPoles = 4.    # NbPoles / 2 = Number of pole pairs (you count the permanent magnets on the rotor to get NbPoles)
    dvf = .7         # aka. freewheeling diode forward voltage
elif pset == 2: #psim
    Inertia = 0.000007            # aka. 'J' in kg/(m^2)
    tau_shaft = 0.006
    Damping = Inertia/tau_shaft   # aka. 'B' in Nm/(rad/s)
    Kv = 1./32.3*1000             # aka. motor constant in RPM/V
    L = 0.00207                   # aka. Coil inductance in H
    M = -0.00069                  # aka. Mutual inductance in H
    R = 11.9                      # aka. Phase resistence in Ohm
    VDC = 300.                    # aka. Supply voltage
    NbPoles = 4.                  #
    dvf = .0                      # aka. freewheeling diode forward voltage
elif pset == 3: #modified psim
    Inertia = 0.000059            # aka. 'J' in kg/(m^2)
    tau_shaft = 0.006
    Damping = Inertia/tau_shaft   # aka. 'B' in Nm/(rad/s)
    Kv = 1./32.3*1000             # aka. motor constant in RPM/V
    L = 0.00207                   # aka. Coil inductance in H
    M = -0.00069                  # aka. Mutual inductance in H
    R = 11.9                      # aka. Phase resistence in Ohm
    VDC = 300.                    # aka. Supply voltage
    NbPoles = 4.                  #
    dvf = .0                      # aka. freewheeling diode forward voltage
else:
    print "Unknown pset {}".format(pset)

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
iv_dhu  = 6
iv_dlu  = 7
iv_dhv  = 8
iv_dlv  = 9
iv_dhw  = 10
iv_dlw  = 11
iv_size = 12


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
ov_theta   = 6
ov_omega   = 7
ov_size    = 8

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

# All diodes conduction vector
adc_uh = 0
adc_ul = 1
adc_vh = 2
adc_vl = 3
adc_wh = 4
adc_wl = 5
adc_size = 6

# Diode conduction vector
dc_h = 0
dc_l = 1
dc_size = 2

#
# Calculate backemf at a given omega offset from the current rotor position
#
# Used to calculate the phase backemf aka. 'e'
#
def backemf(X,thetae_offset):
    phase_thetae = mu.norm_angle((X[sv_theta] * (NbPoles / 2.)) + thetae_offset)

    bemf_constant = mu.vpradps_of_rpmpv(Kv) # aka. ke in V/rad/s
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

def diode(h, l, i, e, star):
    dh = 0
    dl = 0

    if ((h == 0) and (l == 0)):
        if (i < -0.01) or ((e + star) > ((VDC/2) + dvf)):
            dh = 1
            dl = 0
        elif (i > 0.01) or ((e + star) < ((-(VDC/2) - dvf))):
            dh = 0
            dl = 1
        else:
            dh = 0
            dl = 0
    else:
        dh = 0
        dl = 0

    D = [dh, dl]

    return D

def diodes(X, Xdebug, U):

    DU = diode(U[iv_hu], U[iv_lu], X[sv_iu], Xdebug[dv_eu], Xdebug[dv_ph_star])
    DV = diode(U[iv_hv], U[iv_lv], X[sv_iv], Xdebug[dv_ev], Xdebug[dv_ph_star])
    DW = diode(U[iv_hw], U[iv_lw], X[sv_iw], Xdebug[dv_ew], Xdebug[dv_ph_star])

    Ds = [DU[dc_h],
          DU[dc_l],
          DV[dc_h],
          DV[dc_l],
          DW[dc_h],
          DW[dc_l]
          ]

    return Ds

#
# Calculate phase voltages
# Returns a vector of phase voltages in reference to the star point
def voltages(X, U):

    eu = backemf(X, 0.)
    ev = backemf(X, math.pi * (2./3.))
    ew = backemf(X, math.pi * (4./3.))

    # Check which phases are excited
    pux = (U[iv_hu] == 1) or \
        (U[iv_lu] == 1) or \
        (U[iv_dlu] == 1) or \
        (U[iv_dhu] == 1)

    pvx = (U[iv_hv] == 1) or \
        (U[iv_lv] == 1) or \
        (U[iv_dlv] == 1) or \
        (U[iv_dhv] == 1)

    pwx = (U[iv_hw] == 1) or \
        (U[iv_lw] == 1) or \
        (U[iv_dlw] == 1) or \
        (U[iv_dhw] == 1)

    vu = 0.
    vv = 0.
    vw = 0.
    vm = 0.

    if pux and pvx and pwx:
        #print "all phases are conducting!"

        if (U[iv_hu] == 1):
            vu = VDC/2
        elif (U[iv_dhu] == 1):
            vu = VDC/2 + dvf
        elif (U[iv_dlu] == 1):
            vu = -(VDC/2 + dvf)
        else:
            vu = -VDC/2

        if (U[iv_hv] == 1):
            vv = VDC/2
        elif (U[iv_dhv] == 1):
            vv = VDC/2 + dvf
        elif (U[iv_dlv] == 1):
            vv = -(VDC/2 + dvf)
        else:
            vv = -VDC/2

        if (U[iv_hw] == 1):
            vw = VDC/2
        elif (U[iv_dhw] == 1):
            vw = VDC/2 + dvf
        elif (U[iv_dlw] == 1):
            vw = -(VDC/2 + dvf)
        else:
            vw = -VDC/2

        vm = (vu + vv + vw - eu - ev - ew) / 3.

    elif pux and pvx:
        if (U[iv_hu] == 1):
            vu = VDC/2
        elif (U[iv_dhu] == 1):
            vu = VDC/2 + dvf
        elif (U[iv_dlu] == 1):
            vu = -(VDC/2 + dvf)
        else:
            vu = -VDC/2

        if (U[iv_hv] == 1):
            vv = VDC/2
        elif (U[iv_dhv] == 1):
            vv = VDC/2 + dvf
        elif (U[iv_dlv] == 1):
            vv = -(VDC/2 + dvf)
        else:
            vv = -VDC/2

        vm = (vu + vv - eu - ev) / 2.
        vw = ew + vm
    elif pux and pwx:
        if (U[iv_hu] == 1):
            vu = VDC/2
        elif (U[iv_dhu] == 1):
            vu = VDC/2 + dvf
        elif (U[iv_dlu] == 1):
            vu = -(VDC/2 + dvf)
        else:
            vu = -VDC/2

        if (U[iv_hw] == 1):
            vw = VDC/2
        elif (U[iv_dhw] == 1):
            vw = VDC/2 + dvf
        elif (U[iv_dlw] == 1):
            vw = -(VDC/2 + dvf)
        else:
            vw = -VDC/2

        vm = (vu + vw - eu - ew) / 2.
        vv = ev + vm
    elif pvx and pwx:
        if (U[iv_hv] == 1):
            vv = VDC/2
        elif (U[iv_dhv] == 1):
            vv = VDC/2 + dvf
        elif (U[iv_dlv] == 1):
            vv = -(VDC/2 + dvf)
        else:
            vv = -VDC/2

        if (U[iv_hw] == 1):
            vw = VDC/2
        elif (U[iv_dhw] == 1):
            vw = VDC/2 + dvf
        elif (U[iv_dlw] == 1):
            vw = -(VDC/2 + dvf)
        else:
            vw = -VDC/2

        vm = (vv + vw - ev - ew) / 2.
        vu = eu + vm


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
    Xd, Xdebug = dyn_debug(X, t, U, W)

    return Xd

# Dynamic model with debug vector
def dyn_debug(X, t, U, W):

    eu = backemf(X, 0.)
    ev = backemf(X, math.pi * (2./3.))
    ew = backemf(X, math.pi * (4./3.))

    # Electromagnetic torque
    etorque = (eu * X[sv_iu] + ev * X[sv_iv] + ew * X[sv_iw])/X[sv_omega]

    # Acceleration of the rotor
    omega_dot = ((etorque * (NbPoles / 2)) - (Damping * X[sv_omega]) - W[pv_torque]) / Inertia

    V = voltages(X, U)

    pdt = VDC/2 + dvf

    iu_dot = (V[ph_U] - (R * X[sv_iu]) - eu - V[ph_star]) / (L - M)
    iv_dot = (V[ph_V] - (R * X[sv_iv]) - ev - V[ph_star]) / (L - M)
    iw_dot = (V[ph_W] - (R * X[sv_iw]) - ew - V[ph_star]) / (L - M)

    Xd = [  X[sv_omega],
            omega_dot,
            iu_dot,
            iv_dot,
            iw_dot
        ]

    Xdebug = [
        eu,
        ev,
        ew,
        V[ph_U],
        V[ph_V],
        V[ph_W],
        V[ph_star]
        ]

    return Xd, Xdebug


#
#
#
def output(X, U):

    V = voltages(X, U)

    Y = [X[sv_iu], X[sv_iv], X[sv_iw],
         V[ph_U], V[ph_V], V[ph_W],
         X[sv_theta], X[sv_omega]]

    return Y
