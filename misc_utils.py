import math

#
def rad_of_deg(d): return d/180.*math.pi

#
def deg_of_rad(r): return r*180./math.pi
#
def norm_angle(alpha):
    alpha_n = math.fmod(alpha, 2*math.pi)
    return alpha_n
