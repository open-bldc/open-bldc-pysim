import numpy as np

import dyn_model  as dm

PWM_freq = 1000


#
#
# Sp setpoint, Y output
#
def run(Sp, Y, t):

    elec_angle = Y[ov_theta]*dm.NbPoles/3 
    

    U = np.zeros(dm.iv_size)
    return U
