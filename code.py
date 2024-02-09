import board
import analogio

# Initialize the analog pins
left_inductor_pin = analogio.AnalogIn(board.A0)
right_inductor_pin = analogio.AnalogIn(board.A1)

from pid import *
from utils import *

def read_input():
    """Read the difference between the sensor voltages."""
    left_inductor_voltage = get_voltage(left_inductor_pin)
    right_inductor_voltage = get_voltage(right_inductor_pin)
    return left_inductor_voltage - right_inductor_voltage
    
desired_value = 0.0  # The desired value for the PID controller.
pid = PID(kp=0.1, ki=0.01, kd=0.001, setpoint=desired_value)
pid_timer = NonBlockingTimer()
pid_timer.start(0.1)  # Set the desired delay in seconds

while True:
    if pid_timer.is_finished():
        input = read_input()
        output = pid.compute(input)
        # adjust_output(output)  # TODO in motordriver.py
        pid_timer.start(0.1)  # Restart the timer