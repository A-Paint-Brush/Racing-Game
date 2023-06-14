class Bowl:
    def __init__(self):
        self.pos_x = 194
        self.pos_y = 260
        self.width = 95
        self.height = 99

    def left(self):
        if self.pos_x >= 5:
            self.pos_x = self.pos_x - 10

    def right(self):
        if self.pos_x <= 383:
            self.pos_x = self.pos_x + 10
