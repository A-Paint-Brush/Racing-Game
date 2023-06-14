import pygame
import Scratch_Cat
import Ball
import Timer
import path


class Maze:
    def __init__(self, screen, player, clock, lives):
        self.data = []
        self.closed = False
        self.bubble = False
        self.Exit = False
        self.win = False
        self.wall = False
        self.trap = False
        self.mode = ""
        self.cat = Scratch_Cat.ScratchCat()
        self.ball_class = Ball.Ball()
        self.backdrop = pygame.image.load(path.resource_path("Images\\Maze.png"))
        if player == "Orange Cat":
            self.scratch_cat = pygame.transform.scale(pygame.image.load(path.resource_path("Images\\Orange Cat.png")),
                                                      (self.cat.width, self.cat.height))
        else:
            self.scratch_cat = pygame.transform.scale(pygame.image.load(path.resource_path("Images\\Yellow Cat.png")),
                                                      (self.cat.width, self.cat.height))
        self.cat.lives = lives
        self.player = player
        self.ball = pygame.image.load(path.resource_path("Images\\Ball.png"))
        self.font1 = pygame.font.SysFont("Times New Roman", 14)
        self.screen = screen
        self.clock = clock
        self.gameRun = True
        self.game()

    def touching_color_at(self, color, x, y):
        for width in range(0, self.cat.width + 1):
            if x + width < 0 or x + width >= 480:
                return True
            for height in range(0, self.cat.height + 1):
                if y + height < 0 or y + height >= 360:
                    return True
                if self.screen.get_at((x + width, y + height))[0:3] == color:
                    return True
        return False

    def text_bubble(self):
        self.bubble = True
        self.lines = self.data[0]
        self.location = self.data[1]
        self.text = []
        self.text_locations = []
        for item in self.lines:
            self.text.append(self.font1.render(item, False, (0, 0, 0), (255, 255, 255)))
        self.max_width = 0
        for item in self.lines:
            if self.font1.size(item)[0] > self.max_width:
                self.max_width = self.font1.size(item)[0]
        for line in range(0, len(self.text)):
            self.text_locations.append((self.location[0] + 10, self.location[1] + line * 18))
        if self.gameRun:
            pygame.draw.rect(self.screen, (255, 255, 255), [self.location[0], self.location[1], self.max_width + 20, len(self.text) * 18], 0)
            pygame.draw.rect(self.screen, (255, 255, 255), [self.location[0] + 10, self.location[1] - 10, self.max_width, len(self.text) * 18 + 20], 0)
            pygame.draw.circle(self.screen, (255, 255, 255), [self.location[0] + 10, self.location[1]], 10, 0)
            pygame.draw.circle(self.screen, (255, 255, 255), [self.location[0] + self.max_width + 10, self.location[1]], 10, 0)
            pygame.draw.circle(self.screen, (255, 255, 255), [self.location[0] + 10, self.location[1] + len(self.text) * 18], 10, 0)
            pygame.draw.circle(self.screen, (255, 255, 255), [self.location[0] + self.max_width + 10, self.location[1] + len(self.text) * 18], 10, 0)
            if self.mode == "left":
                pygame.draw.polygon(self.screen, (255, 255, 255), [(self.location[0] + 10, self.location[1]), (self.location[0] + 30, self.location[1]), (self.location[0] + 15, self.location[1] - 20)], 0)
            else:
                pygame.draw.polygon(self.screen, (255, 255, 255), [(self.location[0] + self.max_width - 10, self.location[1]), (self.location[0] + self.max_width - 30, self.location[1]), (self.location[0] + self.max_width - 15, self.location[1] - 20)], 0)
            for line in range(0, len(self.text)):
                self.screen.blit(self.text[line], self.text_locations[line])

    def create_text_bubble(self, lines, location, seconds, direction):
        self.data.clear()
        self.data.append(lines)
        self.data.append(location)
        self.data.append(seconds)
        self.mode = direction
        if self.time.get_time() <= seconds:
            self.text_bubble()
        else:
            self.bubble = False
            self.wall = False
            self.trap = False

    def lives(self):
        return self.cat.lives

    def game(self):
        while self.gameRun:
            self.clock.tick(12)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.closed = True
                    self.gameRun = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.cat.is_active():
                        if self.cat.touching_mouse(pygame.mouse.get_pos()):
                            if not self.bubble:
                                self.cat.activate()
            self.screen.fill((255, 255, 255))
            self.screen.blit(self.backdrop, (0, 0))
            Collision = ""
            if self.cat.is_active():
                Collision = self.detect()
                self.cat.go_to_mouse(pygame.mouse.get_pos())
            self.screen.blit(self.scratch_cat, (self.cat.pos_x, self.cat.pos_y))
            self.screen.blit(self.ball, (self.ball_class.pos_x, self.ball_class.pos_y))
            try:
                if Collision == "Wall":
                    self.cat.deactivate()
                    self.cat.reset()
                    if self.cat.lives > 1:
                        if not self.bubble:
                            self.time = Timer.Timer()
                            self.time.reset()
                            self.wall = True
                    self.cat.decrease_lives()
                elif Collision == "Trap":
                    self.cat.reset()
                    if self.cat.lives > 1:
                        if not self.bubble:
                            self.time = Timer.Timer()
                            self.time.reset()
                            self.trap = True
                    self.cat.decrease_lives()
            except:
                pass
            if self.cat.lives <= 0:
                if not self.Exit:
                    self.Exit = True
                    if not self.bubble:
                        self.time = Timer.Timer()
                        self.time.reset()
                        self.Exit = True
            if self.ball_class.collision_check(self.cat.pos_x, self.cat.pos_y, self.cat.width, self.cat.height):
                if not self.Exit:
                    self.Exit = True
                    self.cat.deactivate()
                    if not self.bubble:
                        self.time = Timer.Timer()
                        self.time.reset()
                        self.win = True
            if self.wall:
                self.create_text_bubble(["Don't touch the walls of the cave!", "-1 life! Try again!"], (20, 60), 3,
                                        "left")
            elif self.trap:
                self.create_text_bubble(["Ha! You fell for the trap!", "-1 life! Try taking a different route."],
                                        (20, 60), 3, "left")
            elif self.win:
                self.bubble = True
                self.create_text_bubble(["You did it!", "You may", "continue!"], (self.cat.pos_x - 55, self.cat.pos_y + 50), 3, "right")
            elif self.Exit:
                self.bubble = True
                self.create_text_bubble([self.player + " is so badly injured he can't walk anymore.", "You Lose!"],
                                        (20, 60), 3, "left")
            if self.Exit:
                if not self.bubble:
                    self.gameRun = False
            pygame.display.update()
        if self.closed:
            pygame.quit()

    def detect(self):
        new_pos_x = pygame.mouse.get_pos()[0]
        new_pos_y = pygame.mouse.get_pos()[1]
        if new_pos_x > self.cat.pos_x:
            for x in range(self.cat.pos_x, new_pos_x - self.cat.width // 2 + 1, 1):
                if self.touching_color_at((102, 59, 0), x, self.cat.pos_y) or self.touching_color_at((102, 102, 102), x, self.cat.pos_y):
                    return "Wall"
                elif self.touching_color_at((255, 0, 191), x, self.cat.pos_y) or self.touching_color_at((0, 0, 0), x, self.cat.pos_y) or self.touching_color_at((0, 204, 68), x, self.cat.pos_y) or self.touching_color_at((0, 63, 255), x, self.cat.pos_y):
                    return "Trap"
        else:
            for x in range(self.cat.pos_x, new_pos_x - self.cat.width // 2 + 1, -1):
                if self.touching_color_at((102, 59, 0), x, self.cat.pos_y) or self.touching_color_at((102, 102, 102), x, self.cat.pos_y):
                    return "Wall"
                elif self.touching_color_at((255, 0, 191), x, self.cat.pos_y) or self.touching_color_at((0, 0, 0), x, self.cat.pos_y) or self.touching_color_at((0, 204, 68), x, self.cat.pos_y) or self.touching_color_at((0, 63, 255), x, self.cat.pos_y):
                    return "Trap"
        if new_pos_y > self.cat.pos_y:
            for y in range(self.cat.pos_y, new_pos_y - self.cat.height // 2 + 1, 1):
                if self.touching_color_at((102, 59, 0), self.cat.pos_x, y) or self.touching_color_at((102, 102, 102), self.cat.pos_x, y):
                    return "Wall"
                elif self.touching_color_at((255, 0, 191), self.cat.pos_x, y) or self.touching_color_at((0, 0, 0), self.cat.pos_x, y) or self.touching_color_at((0, 204, 68), self.cat.pos_x, y) or self.touching_color_at((0, 63, 255), self.cat.pos_x, y):
                    return "Trap"
        else:
            for y in range(self.cat.pos_y, new_pos_y - self.cat.height // 2 - 1, -1):
                if self.touching_color_at((102, 59, 0), self.cat.pos_x, y) or self.touching_color_at((102, 102, 102), self.cat.pos_x, y):
                    return "Wall"
                elif self.touching_color_at((255, 0, 191), self.cat.pos_x, y) or self.touching_color_at((0, 0, 0), self.cat.pos_x, y) or self.touching_color_at((0, 204, 68), self.cat.pos_x, y) or self.touching_color_at((0, 63, 255), self.cat.pos_x, y):
                    return "Trap"
