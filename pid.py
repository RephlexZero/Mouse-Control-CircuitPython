import time

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