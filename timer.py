from settings import *


class Timer:
    def __init__(self, duration, repeated=False, func=None):
        self.repeated = repeated
        self.func = func
        self.duration = duration

        self.start_time = 0
        self.active = False

    def activate(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()

    def deactivate(self):
        self.active = False
        self.start_time = 0


    def update(self):
            if not self.active:
                return

            current_time = pygame.time.get_ticks() - self.start_time
            if current_time >= self.duration:
                # calls self.func()
                if self.func is not None:
                    self.func()  # only call once


                # repeating the timer
                if self.repeated:
                    self.activate()
                else:
                    # resetting the timer
                    self.deactivate()

