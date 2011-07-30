import numpy as np

import dyn_model  as dm

import misc_utils as mu

import math

PWM_freq = 8000
PWM_cycle_time = (1./8000)
PWM_duty = 1.
PWM_duty_time = PWM_cycle_time * PWM_duty

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
    if 0. <= elec_angle <= (math.pi * (1./6.)): # second half of step 1
        # U off
        # V low
        # W hpwm
        hu = 0
        lu = 0
        hv = 0
        lv = 1
        if math.fmod(t, PWM_cycle_time) <= PWM_duty_time:
            hw = 1
        else:
            hw = 0
        lw = 0
        step = "1b"
    elif (math.pi * (1.0/6.0)) < elec_angle <= (math.pi * (3.0/6.0)): # step 2
        # U hpwm
        # V low
        # W off
        if math.fmod(t, PWM_cycle_time) <= PWM_duty_time:
            hu = 1
        else:
            hu = 0
        lu = 0
        hv = 0
        lv = 1
        hw = 0
        lw = 0
        step = "2 "
    elif (math.pi * (3.0/6.0)) < elec_angle <= (math.pi * (5.0/6.0)): # step 3
        # U hpwm
        # V off
        # W low
        if math.fmod(t, PWM_cycle_time) <= PWM_duty_time:
            hu = 1
        else:
            hu = 0
        lu = 0
        hv = 0
        lv = 0
        hw = 0
        lw = 1
        step = "3 "
    elif (math.pi * (5.0/6.0)) < elec_angle <= (math.pi * (7.0/6.0)): # step 4
        # U off
        # V hpwm
        # W low
        hu = 0
        lu = 0
        if math.fmod(t, PWM_cycle_time) <= PWM_duty_time:
            hv = 1
        else:
            hv = 0
        lv = 0
        hw = 0
        lw = 1
        step = "4 "
    elif (math.pi * (7.0/6.0)) < elec_angle <= (math.pi * (9.0/6.0)): # step 5
        # U low
        # V hpwm
        # W off
        hu = 0
        lu = 1
        if math.fmod(t, PWM_cycle_time) <= PWM_duty_time:
            hv = 1
        else:
            hv = 0
        lv = 0
        hw = 0
        lw = 0
        step = "5 "
    elif (math.pi * (9.0/6.0)) < elec_angle <= (math.pi * (11.0/6.0)): # step 6
        # U low
        # V off
        # W hpwm
        hu = 0
        lu = 1
        hv = 0
        lv = 0
        if math.fmod(t, PWM_cycle_time) <= PWM_duty_time:
            hw = 1
        else:
            hw = 0
        lw = 0
        step = "6 "
    elif (math.pi * (11.0/6.0)) < elec_angle <= (math.pi * (12.0/6.0)): # first half of step 1
        # U off
        # V low
        # W hpwm
        hu = 0
        lu = 0
        hv = 0
        lv = 1
        if math.fmod(t, PWM_cycle_time) <= PWM_duty_time:
            hw = 1
        else:
            hw = 0
        lw = 0
        step = "1a"
    else:
        print 'ERROR: The electrical angle is out of range!!!'

    # Assigning the scheme phase values to the simulator phases
    # "Connecting the controller wires to the motor" ^^
    # This way we can for example decide which direction we want to turn the motor
    U[dm.iv_hu] = hu
    U[dm.iv_lu] = lu
    U[dm.iv_hv] = hw
    U[dm.iv_lv] = lw
    U[dm.iv_hw] = hv
    U[dm.iv_lw] = lv

    if debug:
        print 'time {} step {} eangle {} switches {}'.format(t, step, mu.deg_of_rad(elec_angle), U)

    return U
