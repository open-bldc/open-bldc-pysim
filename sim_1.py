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

def print_simulation_progress(count, steps):
        sim_perc_last = ((count-1)*100) / steps
        sim_perc = (count*100) / steps
        if (sim_perc_last != sim_perc):
            print "{}%".format(sim_perc)

def copy_diodes(U, D):
    Uout = np.zeros(dm.iv_size)

    Uout[:] = U[:]

    Uout[dm.iv_dhu] = D[dm.adc_uh]
    Uout[dm.iv_dlu] = D[dm.adc_ul]
    Uout[dm.iv_dhv] = D[dm.adc_vh]
    Uout[dm.iv_dlv] = D[dm.adc_vl]
    Uout[dm.iv_dhw] = D[dm.adc_wh]
    Uout[dm.iv_dlw] = D[dm.adc_wl]

    return Uout

def main():
#    t_psim, Y_psim =  mio.read_csv('bldc_startup_psim_1us_resolution.csv')
#    mp.plot_output(t_psim, Y_psim, '.')

    freq_sim = 1e5                              # simulation frequency
    time = pl.arange(0.0, 0.072, 1./freq_sim) # create time slice vector
    X = np.zeros((time.size, dm.sv_size))       # allocate state vector
    Xdebug = np.zeros((time.size, dm.dv_size))  # allocate debug data vector
    Y = np.zeros((time.size, dm.ov_size))       # allocate output vector
    U = np.zeros((time.size, dm.iv_size))       # allocate input vector
    X0 = [0, mu.rad_of_deg(0.1), 0, 0, 0]       #
    X[0,:] = X0
    W = [0]
    D = np.zeros((time.size, dm.adc_size))      # allocate diode conduction vector
    for i in range(1,time.size):

        if i==1:
            Uim2 = np.zeros(dm.iv_size)
        else:
            Uim2 = U[i-2,:]

        Y[i-1,:] = dm.output(X[i-1,:], Uim2)                  # get the output for the last step
        U[i-1,:] = ctl.run(0, Y[i-1,:], time[i-1])            # run the controller for the last step
        D[i-1,:] = dm.diodes(X[i-1,:], Xdebug[i-1], U[i-1,:]) # calculate the diode states based on the last step
        U[i-1,:] = copy_diodes(U[i-1,:], D[i-1,:])            # copy diode conduction states to the input vector
        tmp = integrate.odeint(dm.dyn, X[i-1,:], [time[i-1], time[i]], args=(U[i-1,:], W)) # integrate
        X[i,:] = tmp[1,:] # copy integration output to the current step
        X[i, dm.sv_theta] = mu.norm_angle( X[i, dm.sv_theta]) # normalize the angle in the state
        tmp, Xdebug[i,:] = dm.dyn_debug(X[i-1,:], time[i-1], U[i-1,:], W) # get debug data
        print_simulation_progress(i, time.size)

    Y[-1,:] = Y[-2,:]
    U[-1,:] = U[-2,:]


    mp.plot_output(time, Y, '-')
#    pl.show()
    plt.figure(figsize=(10.24, 5.12))
    display_state_and_command(time, X, U)

    plt.figure(figsize=(10.24, 5.12))
    mp.plot_debug(time, Xdebug)

    plt.figure(figsize=(10.24, 5.12))
    mp.plot_diodes(time, D)

    pl.show()

if __name__ == "__main__":
    main()
