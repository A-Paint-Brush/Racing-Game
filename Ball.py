class Ball:
    def __init__(self):
        self.pos_x = 428
        self.pos_y = 7
        self.width = 46
        self.height = 46

    def collision_check(self, pos_x, pos_y, width, height):
        if pos_x + 16 > self.pos_x and pos_x < self.pos_x + self.width and pos_y > self.pos_y and pos_y < self.pos_y + self.height:
            return True
        else:
            return False
