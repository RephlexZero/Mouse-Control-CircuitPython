def get_voltage(pin):
    """Convert the analog input to voltage."""
    return (pin.value * 3.3) / 65536

class NonBlockingTimer:
    def __init__(self):
        self.start_time = time.monotonic()
        self.delay = 0

    def start(self, delay):
        self.start_time = time.monotonic()
        self.delay = delay

    def is_finished(self):
        return (time.monotonic() - self.start_time) >= self.delay