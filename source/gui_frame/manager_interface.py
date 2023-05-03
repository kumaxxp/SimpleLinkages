class ManagerInterface:
    def __init__(self, speed):
        self.speed = speed

    def set_speed(self, new_speed):
        self.speed = new_speed