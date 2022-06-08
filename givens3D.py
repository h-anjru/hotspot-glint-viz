import math as m
import numpy as np


def givens3D(axis, angle, inverse=False):
    """
    Make a 3-D Givens rotation matrix of given angle [rad] about given axis.

    Input:
        axis [str]: 'x', 'y', or 'z'
        angle [float]: angle of rotation (in radians)
        inverse [bool]: return the inverse of the rotation matrix (for rotation of space)

    Output:
        numpy.ndarray [3x3]

    Reference:
        https://en.wikipedia.org/wiki/Givens_rotation
    """

    # tuple of possible axis values
    axes = ('x', 'y', 'z')

    # check axis input
    if axis not in axes:
        raise ValueError(f"givens3D(): 'axis' must be '{axes[0]}', '{axes[1]}', or '{axes[2]}'")

    # check inverse input
    if not isinstance(inverse, bool):
        raise ValueError("givens3D(): 'inverse' must be of type 'bool'")

    # get cosine and sine values of given angle
    try:
        c, s = m.cos(angle), m.sin(angle)
    except TypeError:
        raise TypeError("givens3D(): 'angle' must be of type 'float'")

    # initialize rotation matrix
    givens_matrix = np.zeros((3, 3))

    # define subscripts of non-zero values
    k = axes.index(axis)  # rotation about k axis...
    i, j = k-2, k-1       # ...on the (i, j) plane (see Reference)

    givens_matrix[k, k] = 1

    givens_matrix[i, i] = c
    givens_matrix[j, j] = c

    givens_matrix[j, i] = s
    givens_matrix[i, j] = -s

    # to rotate the coordinate system instead of vectors, use the inverse of the Givens matrix
    if inverse is True:
        givens_matrix = np.transpose(givens_matrix)  # transpose = inverse for orthogonal matrix

    return givens_matrix
