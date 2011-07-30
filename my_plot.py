
import matplotlib.pyplot as plt

import dyn_model  as dm
import misc_utils as mu

def plot_output(time, Y):
    plt.subplot(4, 1, 1)
    plt.plot(time,Y[:,dm.ov_iu], linewidth=1.5)
    plt.plot(time,Y[:,dm.ov_iv], linewidth=1.5)
    plt.plot(time,Y[:,dm.ov_iw], linewidth=1.5)
    plt.legend(['$i_u$', '$i_v$', '$i_w$'], loc='upper right')
    plt.title('Phase current')
    plt.subplot(4, 1, 2)
    plt.plot(time,Y[:,dm.ov_vu], linewidth=1.5)
    plt.plot(time,Y[:,dm.ov_vv], linewidth=1.5)
    plt.plot(time,Y[:,dm.ov_vw], linewidth=1.5)
    plt.legend(['$v_u$', '$v_v$', '$v_w$'], loc='upper right')
    plt.title('Phase voltage')
 
    plt.subplot(4, 1, 4)
    plt.plot(time,mu.rpm_of_radps(Y[:,dm.ov_omega]), linewidth=1.5)
    plt.title('Rotational Velocity')
       
