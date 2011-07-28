import numpy as np

import dyn_model  as dm

import misc_utils as mu

PWM_freq = 8000


#
#
# Sp setpoint, Y output
#
def run(Sp, Y, t):

    elec_angle = mu.norm_angle(Y[dm.ov_theta]*dm.NbPoles/3) 
    

    U = np.zeros(dm.iv_size)
    return U
