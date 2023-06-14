import random
import Data
import pygame.mixer
import path


def increase_score():
    Data.score = Data.score + 1


class Fish:
    def __init__(self, bowl):
        pygame.mixer.init()
        self.sound = pygame.mixer.Sound(path.resource_path("Sounds\\pop.wav"))
        self.r = random.Random()
        self.bowl = bowl
        self.pos_x = self.r.randint(0, 417)
        self.pos_y = -64
        self.width = 54
        self.height = 42
        self.score = 0
        self.display = True

    def move(self):
        self.pos_y = self.pos_y + 10

    def collision_check(self):
        if self.pos_y >= 360:
            self.display = False
        elif (
                self.bowl.pos_x < self.pos_x + self.width < self.bowl.pos_x + self.bowl.width or self.bowl.pos_x < self.pos_x < self.bowl.pos_x + self.bowl.width or self.bowl.pos_x < self.pos_x + self.width / 2 < self.bowl.pos_x + self.bowl.width) and (
                self.bowl.pos_y < self.pos_y + self.height < self.bowl.pos_y + self.bowl.height or self.bowl.pos_y < self.pos_y < self.bowl.pos_y + self.bowl.height or self.bowl.pos_y < self.pos_y + self.height / 2 < self.bowl.pos_y + self.bowl.height):
            increase_score()
            self.display = False
            try:
                self.sound.play()
            except:
                pass
