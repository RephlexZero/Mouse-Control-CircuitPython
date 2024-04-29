import pwmio
from utils import calculate_max_pwm

class DualMotorController:
    def __init__(self, left_motor_pwm_pin, right_motor_pwm_pin, frequency=1000):
        self.left_motor = pwmio.PWMOut(left_motor_pwm_pin, frequency=frequency, duty_cycle=0)
        self.right_motor = pwmio.PWMOut(right_motor_pwm_pin, frequency=frequency, duty_cycle=0)

    def set_motor_speed(self, motor, speed):
        # Ensure speed is within bounds and set PWM duty cycle
        duty_cycle = min(max(0, speed / 100 * 65535), 65535)
        motor.duty_cycle = int(duty_cycle)

    def set_speeds(self, speed_left, speed_right):
        self.set_motor_speed(self.left_motor, speed_left)
        self.set_motor_speed(self.right_motor, speed_right)

    def drive(self, speed, steering):
        # Positive steering value turns right, negative turns left
        speed_left = speed + steering
        speed_right = speed - steering
        if speed_left > 100:
            speed_right -= speed_left - 100
        elif speed_right > 100:
            speed_left -= speed_right - 100
        speed_left = max(0, min(100, speed_left))
        speed_right = max(0, min(100, speed_right))
        # print("{:.2f} {:.2f}".format(speed_left, speed_right))

        self.set_speeds(speed_left, speed_right)
