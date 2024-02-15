import time
import analogio
import board

vbat_pin = analogio.AnalogIn(board.A2)
max_motor_voltage = 6
potential_divider = 0.5
def calculate_vbat(vbat_pin):
    """Calculate the battery voltage."""
    return (vbat_pin.value * 3.3) / (2 ** 12) / potential_divider

def calculate_max_pwm():
    """Calculate the maximum PWM value based on the battery voltage."""
    vbat_voltage = calculate_vbat(vbat_pin)
    if vbat_voltage == 0:
        return 0
    return (max_motor_voltage / vbat_voltage) * 65535

def read_input(left_sensor_pin, right_sensor_pin):
    """Read the difference between the sensor voltages."""
    left_sensor_voltage = get_voltage(left_sensor_pin)
    right_sensor_voltage = get_voltage(right_sensor_pin)
    return left_sensor_voltage - right_sensor_voltage

def get_voltage(pin):
    """Convert the analog input to voltage."""
    return pin.value * 3.3 / (2 ** 16 - 1)

class NonBlockingTimer:
    def __init__(self):
        self.start_time = time.monotonic()
        self.delay = 0

    def start(self, delay):
        self.start_time = time.monotonic()
        self.delay = delay

    def is_finished(self):
        return (time.monotonic() - self.start_time) >= self.delay