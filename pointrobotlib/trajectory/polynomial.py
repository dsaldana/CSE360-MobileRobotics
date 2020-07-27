import numpy as np


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


def piecewise_2d(X, Y, Vx, Vy, T):
    time, trajectory_x, trajectory_y, trajectory_dx, trajectory_dy = [], [], [], [], []

    # number of time intervals
    n = len(T)

    # For each time interval
    for i in range(n-1):
        # duration of the interval
        duration = T[i + 1] - T[i]
        # Discretizing time in the interval
        dis_time = np.linspace(0, duration, 100, endpoint=False)

        # Compute the coefficients
        poly_x = poly3_coefficients(X[i], Vx[i], X[i + 1], Vx[i + 1], duration)
        poly_y = poly3_coefficients(Y[i], Vy[i],  Y[i + 1], Vy[i + 1], duration)
        # Evaluate trajectory at each time step of the interval
        traj_xi = evaluate_polynomial3(dis_time, poly_x)
        traj_yi = evaluate_polynomial3(dis_time, poly_y)
        # Evaluate derivative
        traj_dxi = evaluate_derivative_poly3(dis_time, poly_x)
        traj_dyi = evaluate_derivative_poly3(dis_time, poly_y)

        trajectory_x += traj_xi.tolist()
        trajectory_y += traj_yi.tolist()
        trajectory_dx += traj_dxi.tolist()
        trajectory_dy += traj_dyi.tolist()

        # time starts at ti
        dis_time += T[i]
        time = dis_time.tolist()

    return time, trajectory_x, trajectory_y, trajectory_dx, trajectory_dy

