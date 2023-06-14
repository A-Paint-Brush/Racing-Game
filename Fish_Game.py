import pygame
import Fish
import Bowl
import threading
import Data
import Timer
import math
import path


def get_score():
    return Data.score


class Main:
    def __init__(self, screen, player, clock):
        Data.score = 0
        self.spawn_timer = Timer.Timer()
        self.spawn_timer.reset()
        self.bowl = Bowl.Bowl()
        self.bowl_timer = Timer.Timer()
        self.bowl_timer.reset()
        self.fish = []
        self.backdrop = pygame.image.load(path.resource_path("Images\\Blue Sky.png"))
        self.fish_image = pygame.transform.scale(pygame.image.load(path.resource_path("Images\\fish.png")), (54, 42))
        if player == "Orange Cat":
            self.bowl_image = pygame.transform.scale(pygame.image.load(path.resource_path("Images\\Big Orange Cat.png")), (self.bowl.width, self.bowl.height))
        else:
            self.bowl_image = pygame.transform.scale(pygame.image.load(path.resource_path("Images\\Big Yellow Cat.png")), (self.bowl.width, self.bowl.height))
        self.screen = screen
        self.clock = clock
        self.gameRun = True
        self.score = 0
        self.right = False
        self.left = False
        self.Exit = False
        self.font = pygame.font.SysFont("Times New Roman", 24)
        self.start_move()
        self.timer = Timer.Timer()
        self.timer.reset()
        while self.gameRun:
            self.clock.tick(12)
            if math.floor(self.spawn_timer.get_time()) >= 1:
                self.spawn()
                self.spawn_timer.reset()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameRun = False
                    for i in self.fish:
                        i.display = False
                    self.Exit = True
                    break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.right = True
                    if event.key == pygame.K_LEFT:
                        self.left = True
                if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
                    self.right = False
                elif event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
                    self.left = False
            for i in range(0, len(self.fish)):
                try:
                    if self.fish[i].display:
                        self.fish[i].move()
                        self.fish[i].collision_check()
                    else:
                        self.fish.pop(i)
                except IndexError:
                    pass
            self.score = get_score()
            self.screen.fill((255, 255, 255))
            self.screen.blit(self.backdrop, (0, 0))
            for i in self.fish:
                if i.display:
                    self.screen.blit(self.fish_image, (i.pos_x, i.pos_y))
            self.screen.blit(self.bowl_image, (self.bowl.pos_x, self.bowl.pos_y))
            self.screen.blit(self.font.render("Score: " + str(self.score) + " , Timer: " + str(math.floor(61 - self.timer.get_time())), False, (0, 0, 0)), (0, 0))
            pygame.display.update()
            if self.timer.get_time() > 60:
                self.gameRun = False
                for i in self.fish:
                    i.display = False
                continue
        if self.Exit:
            pygame.quit()

    def spawn(self):
        self.fish.append(Fish.Fish(self.bowl))

    def move(self):
        while self.gameRun:
            if self.right:
                if self.bowl_timer.get_time() > 0.04:
                    self.bowl.right()
                    self.bowl_timer.reset()
            elif self.left:
                if self.bowl_timer.get_time() > 0.04:
                    self.bowl.left()
                    self.bowl_timer.reset()

    def start_move(self):
        self.thread = threading.Thread(target=self.move)
        self.thread.start()

    def score_data(self):
        return self.score
