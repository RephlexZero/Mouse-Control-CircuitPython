import board
import analogio

from pid import PID
from utils import *
from motor_driver import DualMotorController
    
desired_value = 0.0  # The desired value for the PID controller.
steering_pid = PID(kp=10, ki=0.1, kd=1, setpoint=desired_value)
pid_timer = NonBlockingTimer()
pid_timer.start(0.01)  # Set the desired delay in seconds

left_sensor_pin = analogio.AnalogIn(board.A0)
right_sensor_pin = analogio.AnalogIn(board.A1)

left_motor_pin = board.GP3
right_motor_pin = board.GP4

motors = DualMotorController(left_motor_pin, right_motor_pin)

while True:
    if pid_timer.is_finished():
        input = read_input(left_sensor_pin, right_sensor_pin)
        steering = steering_pid.compute(input)
        speed = 10 # Set the speed from 0% to 100%
        motors.drive(speed, steering)
        pid_timer.start(0.1)  # Restart the timer
        print("Left sensor:", round(get_voltage(left_sensor_pin),2), "Right sensor:", round(get_voltage(right_sensor_pin),2),"Input:", round(input,2), "Steering:", round(steering,2))