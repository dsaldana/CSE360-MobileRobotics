import math
import time
import sim
import numpy as np
from numpy import array
from RobotCoppelia import Robot

# Send force to a robot
r = Robot('bicopterBody')  # Create an instance of our robot

time_steps = 100

# desired height
zd = 1.
vzd = 0
# PID gains
kp = .5
kd = 2
ki = .01
accum_ez = 0
try:
    while r.client_id != -1:

        # Sensing: get position
        x, y, z = r.get_position()
        [vx, vy, vz], Theta = r.get_velocity()

        print( (x, y, z))

        e_z = zd - z
        e_vz = vzd - vz

        u_z = kp * e_z + kd * e_vz + ki * accum_ez
        accum_ez += e_z

        sp = 0.05
        # Control servos and motors
        r.set_servo_forces(servo_angle1=math.pi/2-sp, servo_angle2=math.pi / 2 + sp, force_motor1=u_z, force_motor2=u_z)

        time.sleep(0.05)

except KeyboardInterrupt:
    # Stop motors
    r.set_servo_forces(math.pi/2-.01,math.pi/2+.01,0,0)
    r.close_connection()

