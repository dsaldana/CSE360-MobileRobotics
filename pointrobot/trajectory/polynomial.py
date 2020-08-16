import numpy as np


def poly1_coefficients(x0, xf, tf):
    #TODO
    return

def evaluate_poly1(t, coefficients):
    #TODO
    return




# TODO: test this for vectors
def poly3_coefficients(x0, v0, xf, vf, tf):
    """
    Computes the coefficients of a third degree polynomial based on the initial and final states.
    If x and v are vectors of dimension d, the result are coefficients of the same dimension.
    Same for scalars.
    :param x0: Initial location in 1 coordinate
    :param v0: Initial velocity
    :param xf: Final location
    :param vf: Final velocity
    :param tf: Final time.
    :return: coefficients a0,...,a3.
    """

    a0 = x0
    a1 = v0
    a2 = (3 * xf - 3 * x0 - 2 * v0 * tf - vf * tf) / (tf ** 2)
    a3 = (2 * x0 + (v0 + vf) * tf - 2 * xf) / (tf ** 3)

    return [a0, a1, a2, a3]


def evaluate_polynomial3(t, p3_coefficients):
    [a0, a1, a2, a3] = p3_coefficients
    # Evaluate polynomial at time t
    return a0 + a1 * t + a2 * t ** 2 + a3 * t ** 3


def evaluate_derivative_poly3(t, p3_coefficients):
    [a0, a1, a2, a3] = p3_coefficients
    # Evaluate derivative of the third degree polynomial at time t
    return a1 + 2 * a2 * t + 3 * a3 * t ** 2




