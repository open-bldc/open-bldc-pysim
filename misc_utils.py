#
# Open-BLDC pysim - Open BrushLess DC Motor Controller python simulator
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

import math


#
def rad_of_deg(d):
    return d / 180.0 * math.pi


#
def deg_of_rad(r):
    return r * 180.0 / math.pi


#
def rpm_of_radps(rps):
    return rps / (2 * math.pi) * 60


#
def degps_of_radps(rps):
    return rps / (2 * math.pi) * 60 * 360


#
def radps_of_rpm(rpm):
    return rpm * (2 * math.pi) / 60


#
def vpradps_of_rpmpv(vprpm):
    return 30 / (vprpm * math.pi)


#
def norm_angle(alpha):
    alpha_n = math.fmod(alpha, 2 * math.pi)

    if alpha_n < 0.0:
        alpha_n = (2 * math.pi) + alpha_n

    return alpha_n
