#
# Open-BLDC - Open BrushLess DC Motor Controller
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
