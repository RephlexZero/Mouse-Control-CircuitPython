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
        self.output = 0
        
    def compute(self, input, delta_time):
        
        error = self.setpoint - input
        self.integral += error * delta_time
        derivative = (error - self.last_error) / delta_time
        
        # PID formula
        self.output = (self.kp * error) + (self.ki * self.integral) + (self.kd * derivative)
        
        self.last_error = error
        
        return self.output