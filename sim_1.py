#! /usr/bin/env python

import matplotlib
matplotlib.use('MacOSX')
import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
from scipy import integrate

import misc_utils as mu
import dyn_model  as dm


def display_state(time, X):
    ax = plt.subplot(2,1,1)
    plt.plot(time,mu.deg_of_rad(X[:,dm.sv_alpha]), 'r', linewidth=3.0)
    plt.title('$\\alpha$')
    ax = plt.subplot(2,1,2)
    plt.plot(time,mu.deg_of_rad(X[:,dm.sv_alphad]), 'r', linewidth=3.0)
    plt.title('$\dot{\\alpha}$')
    pl.show()

def main():

    time = pl.arange(0.0, 10., 0.001)
    X0 = [0, mu.rad_of_deg(300)]
    X = np.zeros((time.size, dm.sv_size));
    X[0,:] = X0
    U = [0,0,0,0,0,0]
    W = [0]
    for i in range(1,time.size):
        tmp = integrate.odeint(dm.dyn, X[i-1,:], [time[i-1], time[i]], args=(U, W,))
        X[i,:] = tmp[1,:]
        X[i, dm.sv_alpha] = mu.norm_angle( X[i, dm.sv_alpha])
    display_state(time, X)
        
if __name__ == "__main__":
    main()
