#! /usr/bin/env python

import matplotlib
#matplotlib.use('MacOSX')
#matplotlib.use('GTKCairo')
import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
from scipy import integrate

import misc_utils as mu
import dyn_model  as dm
import control    as ctl
import my_io      as mio
import my_plot    as mp



def display_state_and_command(time, X, U):

    titles_state = ['$\\theta$', '$\omega$', '$i_u$', '$i_v$', '$i_w$']
    titles_cmd = ['$u_l$', '$u_h$', '$v_l$', '$v_h$', '$w_l$', '$w_h$']
    for i in range(0, 2):
        plt.subplot(6, 2, 2*i+1)
        plt.plot(time,mu.deg_of_rad(X[:,i]), 'r', linewidth=3.0)
        plt.title(titles_state[i])
    for i in range(2, dm.sv_size):
        plt.subplot(6, 2, 2*i+1)
        plt.plot(time, X[:,i], 'r', linewidth=3.0)
        plt.title(titles_state[i])
    for i in range(0, 6):
        plt.subplot(6, 2, 2*i+2)
        plt.plot(time, U[:,i], 'r', linewidth=3.0)
        plt.title(titles_cmd[i])


def main():
#    t_psim, Y_psim =  mio.read_csv('bldc_startup_psim_1us_resolution.csv')
#    mp.plot_output(t_psim, Y_psim, '.')

    freq_sim = 1e5
    time = pl.arange(0.0, 0.00016, 1./freq_sim)
    X = np.zeros((time.size, dm.sv_size))
    Xdebug = np.zeros((time.size, dm.dv_size))
    Y = np.zeros((time.size, dm.ov_size))
    U = np.zeros((time.size, dm.iv_size))
    X0 = [0, mu.rad_of_deg(0.1), 0, 0, 0]
    X[0,:] = X0
    W = [0]
    for i in range(1,time.size):
        if i==1:
            Uim2 = [0,0,0,0,0,0,0,0,0,0,0,0]
        else:
            Uim2 = Y[i-2,:]
        Y[i-1,:] = dm.output(X[i-1,:], U[i-2,:])
        U[i-1,:] = ctl.run(0, Y[i-1,:], time[i-1])
        tmp = integrate.odeint(dm.dyn, X[i-1,:], [time[i-1], time[i]], args=(U[i-1,:], W))
        X[i,:] = tmp[1,:]
        X[i, dm.sv_theta] = mu.norm_angle( X[i, dm.sv_theta])
        tmp, Xdebug[i,:] = dm.dyn_debug(X[i-1,:], time[i-1], U[i-1,:], W)
        sim_perc = (((i*1.) / (time.size * 1.) * 100))
        if (sim_perc % 1) == 0:
            print "{}%".format(sim_perc)
    Y[-1,:] = Y[-2,:]
    U[-1,:] = U[-2,:]


    mp.plot_output(time, Y, '-')
#    pl.show()
    plt.figure(figsize=(10.24, 5.12))
    display_state_and_command(time, X, U)

    plt.figure(figsize=(10.24, 5.12))
    mp.plot_debug(time, Xdebug)

    pl.show()

if __name__ == "__main__":
    main()
