import random


class Dice:
    def __init__(self):
        self.r = random.Random()
        self.pos_x = 208
        self.pos_y = 146
        self.width = 64
        self.height = 68
        self.steps = 0
        self.costume = 0
        self.active = True

    def collision_check(self, mouse):
        if self.pos_x < mouse[0] < self.pos_x + self.width and self.pos_y < mouse[1] < self.pos_y + self.height:
            return True
        else:
            return False

    def roll(self):
        self.active = False
        self.steps = self.r.randint(1, 6)
        return self.steps
