from math import pi, cos, sin, sqrt, atan2
import numpy as np
from scipy.ndimage import minimum_filter, maximum_filter
from scipy.spatial.distance import cdist

__author__ = 'tangz'


# default R_earth arg in miles. = 6371 km
def dist(latlon1, latlon2, R_earth=3958.756):
    assert len(latlon1) >= 2 and len(latlon2) >= 2
    # note: if len > 2, only use the first two poitns

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


def minima(mat, mode='wrap', window=10):
    mn = minimum_filter(mat, size=window, mode=mode)
    # (mat == mn) true if pixel is equal to the local min
    mn_indices = np.nonzero(mat == mn)
    return mn_indices, mat[mn_indices]


def maxima(mat, mode='wrap', window=10):
    mx = maximum_filter(mat, size=window, mode=mode)
    # (mat == mx) true if pixel is equal to the local max
    mx_indices = np.nonzero(mat == mx)
    return mx_indices, mat[mx_indices]


def closest_node(node, nodes):
    return nodes[cdist([node], nodes).argmin()]