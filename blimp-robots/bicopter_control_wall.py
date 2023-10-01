
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
                x1, y1 = dist_1 * cos(pi / 6), dist_1 * sin(pi / 6)
                x2, y2 = dist_2 * cos(-pi / 6), dist_2 * sin(-pi / 6)

                # Line y=ax + b
                a = (y1 - y2) / (x1 - x2)
                b = y2 - a * x2
                b = (dist_1 + dist_2) / 2
                # relative angle
                ang = atan2(y1 - y2, x1 - x2)
                # distance

                # desired distance
                dd = 4

                fx = -.1 * (dd - b)
                # fx = 0
                torque = -.01 * (pi / 2 - ang)
                print(degrees(ang), b, fx)







            else:
                torque = rotate
        else:
            if det_2 == True:
                fx = .1
                torque = -rotate
            else:
                fx = 1.4


        # print(front_det,rear_det, fx, sp)


        # force to move forward
        # fx = 0 * .1

        theta = atan2(fz, fx)
        f = hypot(fz, fx)


        # print(math.degrees((theta)), rz, vx)

        base_angle = radians(90)

        # Control servos and motors
        r.set_servo_forces(servo_angle1=theta - torque, servo_angle2=theta + torque, force_motor1=f, force_motor2=f)

        time.sleep(0.001)

except KeyboardInterrupt:
    # Stop motors
    r.set_servo_forces(pi / 2 - .01, pi / 2 + .01, 0, 0)
    r.close_connection()
