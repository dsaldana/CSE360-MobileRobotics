
from math import cos, sin, pi, atan2, radians, hypot, degrees
import time

from RobotCoppelia import Robot

# Send force to a robot


r = Robot('bicopterBody', sensor_names=["proximity_1", "proximity_2"])  # Create an instance of our robot

time_steps = 100

# desired height
zd = 1.
vzd = 0
# desired angular speed
rz_d = .1
kp_z = .1

# PID gains
kp = 1.
kd = 3.
ki = .01
accum_ez = 0
try:
    while r.client_id != -1:

        # Sensing: get position
        x, y, z = r.get_position()
        [vx, vy, vz], [rx, ry, rz] = r.get_velocity()

        # print(z)

        e_z = zd - z
        e_vz = vzd - vz

        fz = kp * e_z + kd * e_vz + ki * accum_ez
        accum_ez += e_z

        e_rz = rz_d - rz
        torque_z = kp_z * e_rz

        (det_1, dist_1), (det_2, dist_2) = r.get_distances()

        torque = 0  #
        rotate = radians(1.)

        if det_1:
            if det_2:
                # fx = 1.4

                # Compute points in the body frame
                beta = pi / 6  # Angle between the y-axis and the ray of the distance sensor.
                x1, y1 = dist_1 * cos(pi / 2 - beta), dist_1 * sin(pi / 2 - beta)  # right point
                x2, y2 = dist_2 * cos(pi / 2 + beta), dist_2 * sin(pi / 2 + beta)  # left point

                # Line y = ax + b
                a = (y1 - y2) / (x1 - x2)
                b = y2 - a * x2     # Distance to the front of the robot (y-axis)
                # b = (dist_1 + dist_2) / 2
                # relative angle
                ang = atan2(y1 - y2, x1 - x2)
                # distance

                # desired distance
                dd = 3.5

                kp_rot = .01
                kp_forward = -.1
                fx = kp_forward * (dd - b)
                torque = kp_rot * (0 - ang)
                print(degrees(ang), b, fx)

            else:
                torque = rotate
        else:
            if det_2:
                fx = .1
                torque = -rotate
            else:
                fx = 1.


        theta = atan2(fz, fx)  # Servo angle
        f = hypot(fz, fx)  # Motor force


        # Control servos and motors
        r.set_servo_forces(servo_angle1=theta - torque, servo_angle2=theta + torque, force_motor1=f, force_motor2=f)

        time.sleep(0.001)

except KeyboardInterrupt:
    # Stop motors
    r.set_servo_forces(pi / 2 - .01, pi / 2 + .01, 0, 0)
    r.close_connection()
