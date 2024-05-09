from random import randint


class Box:
    def __init__(self, s1=0, s2=10):
        self.value = randint(s1, s2)
        self.opened = False

    def open(self):
        if self.opened:
            return None
        self.opened = True
        return self.value
