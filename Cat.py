class Cat:
    def __init__(self, color):
        self.color = color
        if self.color == "Orange":
            self.pos_x = 131
            self.pos_y = 48.5
        else:
            self.pos_x = 97
            self.pos_y = 48.5
        self.width = 38
        self.height = 39
        self.direction = "right"
        self.lives = 3

    def move(self):
        if self.color == "Orange":
            if self.pos_x == 351 and self.pos_y == 48.5:
                self.direction = "down"
            elif self.pos_x == 351 and self.pos_y == 268.5:
                self.direction = "left"
            elif self.pos_x == 131 and self.pos_y == 268.5:
                self.direction = "up"
            elif self.pos_x == 131 and self.pos_y == 48.5:
                self.direction = "right"
            if self.direction == "right":
                self.pos_x = self.pos_x + 110
            elif self.direction == "down":
                self.pos_y = self.pos_y + 110
            elif self.direction == "left":
                self.pos_x = self.pos_x - 110
            else:
                self.pos_y = self.pos_y - 110
        else:
            if self.pos_x == 317 and self.pos_y == 48.5:
                self.direction = "down"
            elif self.pos_x == 317 and self.pos_y == 268.5:
                self.direction = "left"
            elif self.pos_x == 97 and self.pos_y == 268.5:
                self.direction = "up"
            elif self.pos_x == 97 and self.pos_y == 48.5:
                self.direction = "right"
            if self.direction == "right":
                self.pos_x = self.pos_x + 110
            elif self.direction == "down":
                self.pos_y = self.pos_y + 110
            elif self.direction == "left":
                self.pos_x = self.pos_x - 110
            else:
                self.pos_y = self.pos_y - 110
