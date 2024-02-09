import board
import analogio
import time

# Initialize the analog pins
left_inductor_pin = analogio.AnalogIn(board.A0)
right_inductor_pin = analogio.AnalogIn(board.A1)

class PID:
    def __init__(self, kp, ki, kd, setpoint):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.last_error = 0
        self.integral = 0
        self.last_time = time.monotonic()

    def compute(self, input):
        current_time = time.monotonic()
        delta_time = current_time - self.last_time
        if delta_time <= 0.0:
            delta_time = 1.0 # Prevent division by zero
        
        error = self.setpoint - input
        self.integral += error * delta_time
        derivative = (error - self.last_error) / delta_time
        
        # PID formula
        output = (self.kp * error) + (self.ki * self.integral) + (self.kd * derivative)
        
        self.last_error = error
        self.last_time = current_time
        
        return output
    
def get_voltage(pin):
    """Convert the analog input to voltage."""
    return (pin.value * 3.3) / 65536


def read_input():
    """Read the difference between the sensor voltages."""
    left_inductor_voltage = get_voltage(left_inductor_pin)
    right_inductor_voltage = get_voltage(right_inductor_pin)
    return left_inductor_voltage - right_inductor_voltage

class NonBlockingTimer:
    def __init__(self):
        self.start_time = time.monotonic()
        self.delay = 0

    def start(self, delay):
        self.start_time = time.monotonic()
        self.delay = delay

    def is_finished(self):
        return (time.monotonic() - self.start_time) >= self.delay
    
desired_value = 0.0  # The desired value for the PID controller.
pid = PID(kp=0.1, ki=0.01, kd=0.001, setpoint=desired_value)
pid_timer = NonBlockingTimer()
pid_timer.start(0.1)  # Set the desired delay in seconds

while True:
    if pid_timer.is_finished():
        input = read_input()
        output = pid.compute(input)
        adjust_output(output)  # TODO
        pid_timer.start(0.1)  # Restart the timer