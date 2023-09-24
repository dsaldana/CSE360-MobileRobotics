import math
import time
import sim
import numpy as np
from numpy import array
class robot():
    
    def __init__(self, frame_name, motor_names=[], client_id=0):  
        # If there is an existing connection
        if client_id:
                self.client_id = client_id
        else:
            self.client_id = self.open_connection()
            
        self.motors = self._get_handlers(motor_names) 
        
        # Robot frame
        self.frame =  self._get_handler(frame_name)
            
        
    def open_connection(self):
        sim.simxFinish(-1)  # just in case, close all opened connections
        self.client_id = sim.simxStart('127.0.0.1', 19999, True, True, 5000, 5)  # Connect to CoppeliaSim 
        
        if self.client_id != -1:
            print('Robot connected')
        else:
            print('Connection failed')
        return self.client_id
        
    def close_connection(self):    
        sim.simxGetPingTime(self.client_id)  # Before closing the connection to CoppeliaSim, make sure that the last command sent out had time to arrive.
        sim.simxFinish(self.client_id)  # Now close the connection to CoppeliaSim:
        print('Connection closed')
    
    def isConnected(self):
        c,result = sim.simxGetPingTime(self.client_id)
        # Return true if the robot is connected
        return result > 0         
        
    def _get_handler(self, name):
        err_code, handler = sim.simxGetObjectHandle(self.client_id, name, sim.simx_opmode_blocking)
        return handler
    
    def _get_handlers(self, names):
        handlers = []
        for name in names:
            handler = self._get_handler(name)
            handlers.append(handler)
        
        return handlers

    def send_motor_velocities(self, vels):
        for motor, vel in zip(self.motors, vels):
            err_code = sim.simxSetJointTargetVelocity(self.client_id, 
                                                      motor, vel, sim.simx_opmode_streaming)      
            
    def set_position(self, position, relative_object=-1):
        if relative_object != -1:
            relative_object = self._get_handler(relative_object)        
        sim.simxSetObjectPosition(self.client_id, self.frame, relative_object, position, sim.simx_opmode_oneshot)
        
    def simtime(self):
        return sim.simxGetLastCmdTime(self.client_id)
    
    def get_position(self, relative_object=-1):
        # Get position relative to an object, -1 for global frame
        if relative_object != -1:
            relative_object = self._get_handler(relative_object)
        res, position = sim.simxGetObjectPosition(self.client_id, self.frame, relative_object, sim.simx_opmode_blocking)        
        return np.array(position)
    
    def get_velocity(self, relative_object=-1):
        # Get velocity relative to an object, -1 for global frame
        if relative_object != -1:
            relative_object = self._get_handler(relative_object)
        res, velocity, omega = sim.simxGetObjectVelocity(self.client_id, self.frame, sim.simx_opmode_blocking)        
        return array(velocity), array(omega)
    
    
    
    def get_object_position(self, object_name):
        # Get Object position in the world frame
        err_code, object_h = sim.simxGetObjectHandle(self.client_id, object_name, sim.simx_opmode_blocking)
        res, position = sim.simxGetObjectPosition(self.client_id, object_h, -1, sim.simx_opmode_blocking)
        return array(position)
    
    def get_object_relative_position(self, object_name):        
        # Get Object position in the robot frame
        err_code, object_h = sim.simxGetObjectHandle(self.client_id, object_name, sim.simx_opmode_blocking)
        res, position = sim.simxGetObjectPosition(self.client_id, object_h, self.frame, sim.simx_opmode_blocking)
        return array(position)
    
    def set_float(self, f, signal='f'):
        return sim.simxSetFloatSignal(self.client_id, signal, f, sim.simx_opmode_oneshot)
    

    def set_servo_forces(self, servo_angle1, servo_angle2, force_motor1, force_motor2):
        self.set_float(force_motor1, 'f1')  # Force motor 1
        self.set_float(force_motor2, 'f2')  # Force motor 2
        self.set_float(servo_angle1, 't1')  # Servo 1
        self.set_float(servo_angle2, 't2')  # Servo 2

    

# Send force to a robot
r = robot('bicopterBody')  # Create an instance of our robot

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


        e_rz= rz_d - rz
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

