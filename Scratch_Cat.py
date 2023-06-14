class ScratchCat:
    def __init__(self):
        self.width = 16
        self.height = 17
        self.pos_x = 21
        self.pos_y = 15
        self.follow_mouse = False
        self.lives = 3

    def go_to_mouse(self, mouse):
        if self.width // 2 < mouse[0] < 480 - self.width // 2 and 0 + self.height // 2 < mouse[1] < 360 - self.height // 2:
            if self.follow_mouse:
                if abs(self.pos_x - mouse[0]) <= 50 and abs(self.pos_y - mouse[1]) <= 50:
                    self.pos_x = mouse[0] - self.width // 2
                    self.pos_y = mouse[1] - self.height // 2

    def touching_mouse(self, mouse):
        if self.pos_x < mouse[0] < self.pos_x + self.width and self.pos_y < mouse[1] < self.pos_y + self.height:
            return True
        else:
            return False

    def activate(self):
        self.follow_mouse = True

    def deactivate(self):
        self.follow_mouse = False

    def is_active(self):
        return self.follow_mouse

    def decrease_lives(self):
        self.lives = self.lives - 1

    def reset(self):
        self.pos_x = 21
        self.pos_y = 15
        self.follow_mouse = False
