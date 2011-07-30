
import numpy      as np
import dyn_model  as dm
import misc_utils as mu

def read_csv(filename):
    my_records = np.recfromcsv(filename)
    Y = np.zeros((my_records.time.size, dm.ov_size))
    Y[:,dm.ov_iu] = my_records.ia
    Y[:,dm.ov_iv] = my_records.ib
    Y[:,dm.ov_iw] = my_records.ic
    Y[:,dm.ov_vu] = my_records.vag
    Y[:,dm.ov_vv] = my_records.vbg
    Y[:,dm.ov_vw] = my_records.vcg
    Y[:,dm.ov_omega] = mu.radps_of_rpm(my_records.nm)
#    import code; code.interact(local=locals())
    return my_records.time, Y
