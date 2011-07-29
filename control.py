import numpy as np

import dyn_model  as dm

import misc_utils as mu

import math

PWM_freq = 8000

debug = False

#
#
# Sp setpoint, Y output
#
def run(Sp, Y, t):

    elec_angle = mu.norm_angle(Y[dm.ov_theta] * dm.NbPoles/2)

    U = np.zeros(dm.iv_size)

    step = "none"

    # switching pattern based on the "encoder"
    # H PWM L ON pattern
    # 100% duty cycle for now needs to be variable and stuff ^^
    #if (elec_angle > 0) and (elec_angle <= (math.pi * (1/6))): # second half of step 1
    if 0. <= elec_angle <= (math.pi * (1./6.)): # second half of step 1
        # U off
        # V low
        # W hpwm (100% duty for now)
        U[dm.iv_hu] = 0
        U[dm.iv_lu] = 0
        U[dm.iv_hv] = 0
        U[dm.iv_lv] = 1
        U[dm.iv_hw] = 1
        U[dm.iv_lw] = 0
        step = "1b"
    elif (math.pi * (1.0/6.0)) < elec_angle <= (math.pi * (3.0/6.0)): # step 2
        # U hpwm
        # V low
        # W off
        U[dm.iv_hu] = 1
        U[dm.iv_lu] = 0
        U[dm.iv_hv] = 0
        U[dm.iv_lv] = 1
        U[dm.iv_hw] = 0
        U[dm.iv_lw] = 0
        step = "2 "
    elif (math.pi * (3.0/6.0)) < elec_angle <= (math.pi * (5.0/6.0)): # step 3
        # U hpwm
        # V off
        # W low
        U[dm.iv_hu] = 1
        U[dm.iv_lu] = 0
        U[dm.iv_hv] = 0
        U[dm.iv_lv] = 0
        U[dm.iv_hw] = 0
        U[dm.iv_lw] = 1
        step = "3 "
    elif (math.pi * (5.0/6.0)) < elec_angle <= (math.pi * (7.0/6.0)): # step 4
        # U off
        # V hpwm
        # W low
        U[dm.iv_hu] = 0
        U[dm.iv_lu] = 0
        U[dm.iv_hv] = 1
        U[dm.iv_lv] = 0
        U[dm.iv_hw] = 0
        U[dm.iv_lw] = 1
        step = "4 "
    elif (math.pi * (7.0/6.0)) < elec_angle <= (math.pi * (9.0/6.0)): # step 5
        # U low
        # V hpwm
        # W off
        U[dm.iv_hu] = 0
        U[dm.iv_lu] = 1
        U[dm.iv_hv] = 1
        U[dm.iv_lv] = 0
        U[dm.iv_hw] = 0
        U[dm.iv_lw] = 0
        step = "5 "
    elif (math.pi * (9.0/6.0)) < elec_angle <= (math.pi * (11.0/6.0)): # step 6
        # U low
        # V off
        # W hpwm
        U[dm.iv_hu] = 0
        U[dm.iv_lu] = 1
        U[dm.iv_hv] = 0
        U[dm.iv_lv] = 0
        U[dm.iv_hw] = 1
        U[dm.iv_lw] = 0
        step = "6 "
    elif (math.pi * (11.0/6.0)) < elec_angle <= (math.pi * (12.0/6.0)): # first half of step 1
        # U off
        # V low
        # W hpwm
        U[dm.iv_hu] = 0
        U[dm.iv_lu] = 0
        U[dm.iv_hv] = 0
        U[dm.iv_lv] = 1
        U[dm.iv_hw] = 1
        U[dm.iv_lw] = 0
        step = "1a"
    else:
        print 'ERROR: The electrical angle is out of range!!!'

    if debug:
        print 'step {} {} {}'.format(step, mu.deg_of_rad(elec_angle), U)

    return U
