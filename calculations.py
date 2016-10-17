from math import pi, cos, sin, sqrt, atan2

__author__ = 'tangz'


def dist_mi(latlon1, latlon2):
    assert len(latlon1) >= 2 and len(latlon2) >= 2
    # note: if len > 2, only use the first two poitns

    # use miles as units for now
    R_earth = 3958.756  # =6371 km

    def to_radians(deg):
        return pi / 180 * deg

    lat1, lat2 = latlon1[0], latlon2[0]
    lon1, lon2 = latlon1[1], latlon2[1]
    phi1, phi2 = to_radians(lat1), to_radians(lat2)

    dphi = to_radians(lat2 - lat1)
    dlambda = to_radians(lon2 - lon1)

    a = sin(dphi / 2)**2 + cos(phi1) * cos(phi2) * sin(dlambda / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return c * R_earth


