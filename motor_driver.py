import pwmio
from utils import calculate_max_pwm

class DualMotorController:
    def __init__(self, motor_a_pwm_pin, motor_b_pwm_pin, frequency=5000):
        self.motor_a = pwmio.PWMOut(motor_a_pwm_pin, frequency=frequency, duty_cycle=0)
        self.motor_b = pwmio.PWMOut(motor_b_pwm_pin, frequency=frequency, duty_cycle=0)

    def set_motor_speed(self, motor, speed):
        # Ensure speed is within bounds and set PWM duty cycle
        duty_cycle = min(max(0, speed / 100 * 65535), 65535)
        motor.duty_cycle = int(duty_cycle)

    def set_speeds(self, speed_a, speed_b):
        self.set_motor_speed(self.motor_a, speed_a)
        self.set_motor_speed(self.motor_b, speed_b)

    def drive(self, speed, steering):
        speed_a = speed + steering
        speed_b = speed - steering
        self.set_speeds(speed_a, speed_b)
