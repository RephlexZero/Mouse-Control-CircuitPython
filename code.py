import board
import analogio
import time

from pid import PID
from utils import *
from motor_driver import DualMotorController
    
left_sensor_pin = analogio.AnalogIn(board.A0)
right_sensor_pin = analogio.AnalogIn(board.A1)

left_motor_pin = board.GP14
right_motor_pin = board.GP0

for i in range(10):
    desired_value = read_input(left_sensor_pin, right_sensor_pin)
# Safe
steering_pid = PID(kp=25, ki=0, kd=7, setpoint=desired_value) # Safe
speed =  30 # Set the speed from 0% to 100%

# steering_pid = PID(kp=23, ki=0, kd=8, setpoint=desired_value) # Safe
# speed =  50 # Set the speed from 0% to 100%


motors = DualMotorController(left_motor_pin, right_motor_pin)

last_time = time.monotonic()
while True:
    now = time.monotonic()
    delta_time = now - last_time
    if delta_time < 0.01:
        continue
    input = read_input(left_sensor_pin, right_sensor_pin)
    steering = steering_pid.compute(input, delta_time)
    motors.drive(speed, steering)
    print("Input: {:.2f} Steering: {:.2f} Speed: {:.2f}".format(input, steering, speed))
    last_time = now