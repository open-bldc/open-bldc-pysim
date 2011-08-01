import math

#
def rad_of_deg(d): return d/180.*math.pi

#
def deg_of_rad(r): return r*180./math.pi

#
def rpm_of_radps(rps): return rps/(2*math.pi)*60

#
def degps_of_radps(rps): return rps/(2*math.pi)*60*360

#
def radps_of_rpm(rpm): return rpm*(2*math.pi)/60

#
def vpradps_of_rpmpv(vprpm): return 30/(vprpm*math.pi)

#
def norm_angle(alpha):
    alpha_n = math.fmod(alpha, 2*math.pi)

    if alpha_n < 0.:
        alpha_n = (2*math.pi) + alpha_n

    return alpha_n
