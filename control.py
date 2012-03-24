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

import dyn_model  as dm

import misc_utils as mu

import math

PWM_freq = 200000
PWM_cycle_time = (1./200000)
PWM_duty = .75
PWM_duty_time = PWM_cycle_time * PWM_duty

debug = False

#
#
# Sp setpoint, Y output
#
def run_hpwm_l_on_bipol(Sp, Y, t):
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

#
#
# Sp setpoint, Y output
#
def run_hpwm_l_on(Sp, Y, t):
    elec_angle = mu.norm_angle(Y[dm.ov_theta] * dm.NbPoles/2)

    U = np.zeros(dm.iv_size)

    step = "none"

    # switching pattern based on the "encoder"
    # H PWM L ON pattern bipolar
    if 0. <= elec_angle <= (math.pi * (1./6.)): # second half of step 1
        # U off
        # V low
        # W hpwm
        hu = 0
        lu = 0
        if math.fmod(t, PWM_cycle_time) <= PWM_duty_time:
            hw = 1
	    lw = 0
            hv = 0
            lv = 1
        else:
            hw = 0
            lw = 1
            hv = 1
            lv = 0
        step = "1b"
    elif (math.pi * (1.0/6.0)) < elec_angle <= (math.pi * (3.0/6.0)): # step 2
        # U hpwm
        # V low
        # W off
        if math.fmod(t, PWM_cycle_time) <= PWM_duty_time:
            hu = 1
	    lu = 0
            hv = 0
            lv = 1
        else:
            hu = 0
	    lu = 1
            hv = 1
            lv = 0
        hw = 0
        lw = 0
        step = "2 "
    elif (math.pi * (3.0/6.0)) < elec_angle <= (math.pi * (5.0/6.0)): # step 3
        # U hpwm
        # V off
        # W low
        if math.fmod(t, PWM_cycle_time) <= PWM_duty_time:
            hu = 1
            lu = 0
            hw = 0
            lw = 1
        else:
            hu = 0
            lu = 1
            hw = 1
            lw = 0
        hv = 0
        lv = 0
        step = "3 "
    elif (math.pi * (5.0/6.0)) < elec_angle <= (math.pi * (7.0/6.0)): # step 4
        # U off
        # V hpwm
        # W low
        hu = 0
        lu = 0
        if math.fmod(t, PWM_cycle_time) <= PWM_duty_time:
            hv = 1
            lv = 0
            hw = 0
            lw = 1
        else:
            hv = 0
            lv = 1
            hw = 1
            lw = 0
        step = "4 "
    elif (math.pi * (7.0/6.0)) < elec_angle <= (math.pi * (9.0/6.0)): # step 5
        # U low
        # V hpwm
        # W off
        if math.fmod(t, PWM_cycle_time) <= PWM_duty_time:
            hv = 1
            lv = 0
            hu = 0
            lu = 1
        else:
            hv = 0
            lv = 1
            hu = 1
            lu = 0
        hw = 0
        lw = 0
        step = "5 "
    elif (math.pi * (9.0/6.0)) < elec_angle <= (math.pi * (11.0/6.0)): # step 6
        # U low
        # V off
        # W hpwm
        hv = 0
        lv = 0
        if math.fmod(t, PWM_cycle_time) <= PWM_duty_time:
            hw = 1
            lw = 0
            hu = 0
            lu = 1
        else:
            hw = 0
            lw = 1
            hu = 1
            lu = 0
        step = "6 "
    elif (math.pi * (11.0/6.0)) < elec_angle <= (math.pi * (12.0/6.0)): # first half of step 1
        # U off
        # V low
        # W hpwm
        hu = 0
        lu = 0
        if math.fmod(t, PWM_cycle_time) <= PWM_duty_time:
            hw = 1
            lw = 0
            hv = 0
            lv = 1
        else:
            hw = 0
            lw = 1
            hv = 1
            lv = 0
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


#
#
# Sp setpoint, Y output
#
def run(Sp, Y, t):
    #return run_hpwm_l_on(Sp, Y, t)
    return run_hpwm_l_on_bipol(Sp, Y, t)
