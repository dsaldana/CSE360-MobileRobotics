import math
import time

from RobotCoppelia import Robot

# Send force to a robot



r = Robot('bicopterBody')  # Create an instance of our robot

time_steps = 100

# desired height
zd = 1.
vzd = 0
# desired angular speed
rz_d = .1
kp_z =.1

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

        # force to move forward
        fx = .1


        theta = math.atan2(fz, fx)
        f = math.hypot(fz,fx)

        print(math.degrees((theta)), rz, vx)

        base_angle = math.radians(90)
        sp = math.radians(3)
        # Control servos and motors
        r.set_servo_forces(servo_angle1=theta, servo_angle2=theta+sp, force_motor1=f, force_motor2=f)

        time.sleep(0.001)

except KeyboardInterrupt:
    # Stop motors
    r.set_servo_forces(math.pi/2-.01,math.pi/2+.01,0,0)
    r.close_connection()

