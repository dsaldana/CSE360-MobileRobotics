import numpy as np


def poly1_coefficients(x0, xf, tf):
    # TODO
    return


def evaluate_poly1(t, coefficients):
    # TODO
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
    # Convert to numpy
    x0 = np.array(x0)
    v0 = np.array(v0)
    xf = np.array(xf)
    vf = np.array(vf)

    a0 = x0
    a1 = v0
    a2 = (3 * xf - 3 * x0 - 2 * v0 * tf - vf * tf) / (tf ** 2)
    a3 = (2 * x0 + (v0 + vf) * tf - 2 * xf) / (tf ** 3)

    return [a0, a1, a2, a3]





def evaluate_polynomial3_vector(t, p3_coefficients):
    """
    Evaluate a polynomial at time t. If time is not an scalar value, we have to clone it to multiple columns, so we can
    use the dot product.

    This would be the code without vector form:
    return a0 + a1 * t + a2 * t ** 2 + a3 * t ** 3

    :param t: time, scalar or vector
    :param p3_coefficients:
    :return:
    """
    t = np.array(t)
    [a0, a1, a2, a3] = np.array(p3_coefficients)

    # Clone time to use dot product
    if a0.size > 1:
        t = np.vstack((t for _ in a0))

    # Evaluate polynomial at time t
    return np.dot(a0, np.ones(len(t))) + np.dot(a1, t) + np.dot(a2, t ** 2) + np.dot(a3, t ** 3)


def evaluate_derivative_poly3(t, p3_coefficients):
    [a0, a1, a2, a3] = p3_coefficients
    # Evaluate derivative of the third degree polynomial at time t
    # FIXME change to vector form using dot product
    return a1 + 2 * a2 * t + 3 * a3 * t ** 2

#
# Initial and final waypoints.
P0 = [0, 0]
Pf = [8, 8]
V0 = [2.5, -2.5]
Vf = [0, 2.51]

tf = 8

# Compute coefficients
coeff = poly3_coefficients(P0, V0, Pf, Vf, tf)

# Evaluate polynomial in the time interval
t = np.linspace(0, tf, 30)

traj = evaluate_polynomial3(t, coeff)

print(traj.shape)
# [a0, a1, a2, a3] = coeff
# np.dot(a0, txy)




def evaluate_polynomial3_vector(t, p3_coefficients):
    """
    Evaluate a polynomial at time t. If time is not an scalar value, we have to clone it to multiple columns, so we can
    use the dot product.

    This would be the code without vector form:
    return a0 + a1 * t + a2 * t ** 2 + a3 * t ** 3

    :param t: time, scalar or vector
    :param p3_coefficients:
    :return:
    """
    t = np.array(t)
    [a0, a1, a2, a3] = np.array(p3_coefficients)

    # Clone time to use dot product
    if a0.size > 1:
        t = np.vstack((t for _ in a0))

    # Evaluate polynomial at time t
    return np.dot(a0, np.ones(len(t))) + np.dot(a1, t) + np.dot(a2, t ** 2) + np.dot(a3, t ** 3)
