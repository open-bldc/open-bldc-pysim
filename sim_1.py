#! /usr/bin/env python

import matplotlib
#matplotlib.use('MacOSX')
matplotlib.use('GTKCairo')
import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
from scipy import integrate

import misc_utils as mu
import dyn_model  as dm
import control    as ctl


def display_state(time, X):
    ax = plt.subplot(2,1,1)
    plt.plot(time,mu.deg_of_rad(X[:,dm.sv_theta]), 'r', linewidth=3.0)
    plt.title('$\\alpha$')
    ax = plt.subplot(2,1,2)
    plt.plot(time,mu.deg_of_rad(X[:,dm.sv_omega]), 'r', linewidth=3.0)
    plt.title('$\dot{\\alpha}$')
    pl.show()

def main():

    time = pl.arange(0.0, 10., 0.001)
    X = np.zeros((time.size, dm.sv_size))
    Y = np.zeros((time.size, dm.ov_size))
    U = np.zeros((time.size, dm.iv_size)) 
    X0 = [0, mu.rad_of_deg(300), 0, 0, 0]
    X[0,:] = X0
    W = [0]
    for i in range(1,time.size):
        Y[i-1,:] = dm.output(X[i-1,:])
        U[i-1,:] = ctl.run(0, Y[i-1,:], time[i-1]) 
        tmp = integrate.odeint(dm.dyn, X[i-1,:], [time[i-1], time[i]], args=(U[i-1,:], W,))
        X[i,:] = tmp[1,:]
        X[i, dm.sv_theta] = mu.norm_angle( X[i, dm.sv_theta])

    display_state(time, X)
        
if __name__ == "__main__":
    main()
