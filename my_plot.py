
import matplotlib.pyplot as plt

import dyn_model  as dm
import misc_utils as mu

def plot_output(time, Y, ls):
    plt.subplot(4, 1, 1)
    plt.plot(time,Y[:,dm.ov_iu], ls, linewidth=1.5)
    plt.plot(time,Y[:,dm.ov_iv], ls, linewidth=1.5)
    plt.plot(time,Y[:,dm.ov_iw], ls, linewidth=1.5)
    plt.legend(['$i_u$', '$i_v$', '$i_w$'], loc='upper right')
    plt.title('Phase current')
    plt.subplot(4, 1, 2)
    plt.plot(time,Y[:,dm.ov_vu], ls, linewidth=1.5)
    plt.plot(time,Y[:,dm.ov_vv], ls, linewidth=1.5)
    plt.plot(time,Y[:,dm.ov_vw], ls, linewidth=1.5)
    plt.legend(['$v_u$', '$v_v$', '$v_w$'], loc='upper right')
    plt.title('Phase voltage')
 
    plt.subplot(4, 1, 4)
    plt.plot(time,mu.rpm_of_radps(Y[:,dm.ov_omega]), ls, linewidth=1.5)
    plt.title('Rotational Velocity')
       
