import pygame
import threading
import time
import Dice
import Cat
import Maze_Game
import Fish_Game
import Timer
import random
import path


class Main:
    def __init__(self):
        self.page = 0
        self.first_loop = True
        self.bubble = False
        self.thread = None
        self.run = True
        self.trap1 = False
        self.trap2 = False
        self.max_width = 0
        self.current_game = "Instructions"
        pygame.init()
        self.dice = Dice.Dice()
        self.orange_cat = Cat.Cat("Orange")
        self.yellow_cat = Cat.Cat("Yellow")
        self.steps = 0
        self.player = "Orange Cat"
        self.orange_cat.lives = 3
        self.font1 = pygame.font.SysFont("Times New Roman", 18)
        self.small_font = pygame.font.SysFont("Times New Roman", 11)
        self.backdrop = pygame.image.load(path.resource_path("Images\\Grass field.png"))
        self.orange_cat_img = pygame.transform.scale(pygame.image.load(path.resource_path("Images\\Orange Cat.png")),
                                                     (self.orange_cat.width, self.orange_cat.height))
        self.yellow_cat_img = pygame.transform.scale(pygame.image.load(path.resource_path("Images\\Yellow Cat.png")),
                                                     (self.yellow_cat.width, self.yellow_cat.height))
        self.dice1_img = pygame.image.load(path.resource_path("Images\\Dice1.png"))
        self.dice2_img = pygame.image.load(path.resource_path("Images\\Dice2.png"))
        self.dice3_img = pygame.image.load(path.resource_path("Images\\Dice3.png"))
        self.dice4_img = pygame.image.load(path.resource_path("Images\\Dice4.png"))
        self.dice5_img = pygame.image.load(path.resource_path("Images\\Dice5.png"))
        self.dice6_img = pygame.image.load(path.resource_path("Images\\Dice6.png"))
        self.orange_cat_win_screen = pygame.image.load(path.resource_path("Images\\Orange cat wins.png"))
        self.yellow_cat_win_screen = pygame.image.load(path.resource_path("Images\\Yellow cat wins.png"))
        self.orange_cat_lose = pygame.image.load(path.resource_path("Images\\Orange cat out of lives.png"))
        self.yellow_cat_lose = pygame.image.load(path.resource_path("Images\\Yellow cat out of lives.png"))
        self.dice_costumes = [self.dice1_img,
                              self.dice2_img,
                              self.dice3_img,
                              self.dice4_img,
                              self.dice5_img,
                              self.dice6_img]
        pygame.display.set_caption("Racing Game")
        self.screen = pygame.display.set_mode((480, 360))
        self.clock = pygame.time.Clock()
        self.data = []
        self.mode = ""
        self.closed = False
        self.trap1_init = True
        self.trap2_init = True
        self.ball = pygame.image.load(path.resource_path("Images\\Ball.png"))
        self.gameRun = True
        self.direction = ""
        self.game()

    def game(self):
        while self.gameRun:
            if self.current_game == "Main":
                self.clock.tick(12)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.gameRun = False
                        break
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if self.dice.collision_check(pygame.mouse.get_pos()):
                            if self.dice.active:
                                self.steps = self.dice.roll()
                                self.move_player()
                if self.trap1:
                    if self.trap1_init:
                        self.trap1_timer = Timer.Timer()
                        self.trap1_timer.reset()
                        self.trap1_init = False
                    if self.player == "Orange Cat":
                        self.square_trap("Yellow Cat")
                    else:
                        self.square_trap("Orange Cat")
                elif self.trap2:
                    if self.trap2_init:
                        self.trap2_timer = Timer.Timer()
                        self.trap2_timer.reset()
                        self.trap2_init = False
                    if self.player == "Orange Cat":
                        self.square_trap2("Yellow Cat")
                    else:
                        self.square_trap2("Orange Cat")
                if self.orange_cat.lives <= 0:
                    self.player = "Orange Cat"
                    self.lose_timer = Timer.Timer()
                    self.lose_timer.reset()
                    self.current_game = "Lose"
                elif self.yellow_cat.lives <= 0:
                    self.player = "Yellow Cat"
                    self.lose_timer = Timer.Timer()
                    self.lose_timer.reset()
                    self.current_game = "Lose"
                self.screen.fill((255, 255, 255))
                self.screen.blit(self.backdrop, (0, 0))
                pygame.draw.rect(self.screen, (179, 179, 179), [83, 23, 94, 94], 0)
                pygame.draw.rect(self.screen, (179, 179, 179), [194, 23, 94, 94], 0)
                pygame.draw.rect(self.screen, (179, 179, 179), [304, 23, 94, 94], 0)
                pygame.draw.rect(self.screen, (179, 179, 179), [304, 133, 94, 94], 0)
                pygame.draw.rect(self.screen, (179, 179, 179), [304, 243, 94, 94], 0)
                pygame.draw.rect(self.screen, (179, 179, 179), [194, 243, 94, 94], 0)
                pygame.draw.rect(self.screen, (179, 179, 179), [83, 243, 94, 94], 0)
                if self.trap1:
                    self.screen.blit(self.small_font.render("Move back 4 steps!",
                                                            True,
                                                            (0, 0, 0)), (85, 245))
                pygame.draw.rect(self.screen, (179, 179, 179), [83, 133, 94, 94], 0)
                if self.trap2:
                    self.screen.blit(self.small_font.render("Move back 1 step!",
                                                            True,
                                                            (0, 0, 0)), (85, 135))
                self.screen.blit(self.dice_costumes[self.dice.costume - 1], (self.dice.pos_x, self.dice.pos_y))
                self.screen.blit(self.orange_cat_img, (int(self.orange_cat.pos_x), int(self.orange_cat.pos_y)))
                self.screen.blit(self.yellow_cat_img, (int(self.yellow_cat.pos_x), int(self.yellow_cat.pos_y)))
                self.screen.blit(self.font1.render("It's " + self.player + "'s turn to move.",
                                                   True,
                                                   (0, 0, 0),
                                                   (109, 255, 102)),
                                 (20, 2))
                self.screen.blit(self.font1.render(str(self.orange_cat.lives), True, (0, 0, 0), (109, 255, 102)),
                                 (80, 339))
                self.screen.blit(self.font1.render(str(self.yellow_cat.lives),
                                                   True,
                                                   (0, 0, 0),
                                                   (109, 255, 102)),
                                 (438, 339))
                if self.gameRun:
                    pygame.display.update()
            elif self.current_game == "Number":
                if self.first_loop:
                    Input = ""
                    self.number_exit = False
                    self.small = False
                    self.big = False
                    self.correct = False
                    self.answer_correct = False
                    number = random.randint(1, 100)
                    caret_display = True
                    caret_timer = Timer.Timer()
                    caret_timer.reset()
                    self.first_loop = False
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.gameRun = False
                        break
                    elif event.type == pygame.KEYDOWN:
                        if len(Input) <= 2:
                            if not self.number_exit:
                                if event.key == pygame.K_0 or event.key == pygame.K_KP0:
                                    Input = Input + "0"
                                elif event.key == pygame.K_1 or event.key == pygame.K_KP1:
                                    Input = Input + "1"
                                elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                                    Input = Input + "2"
                                elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                                    Input = Input + "3"
                                elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                                    Input = Input + "4"
                                elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
                                    Input = Input + "5"
                                elif event.key == pygame.K_6 or event.key == pygame.K_KP6:
                                    Input = Input + "6"
                                elif event.key == pygame.K_7 or event.key == pygame.K_KP7:
                                    Input = Input + "7"
                                elif event.key == pygame.K_8 or event.key == pygame.K_KP8:
                                    Input = Input + "8"
                                elif event.key == pygame.K_9 or event.key == pygame.K_KP9:
                                    Input = Input + "9"
                        if not self.number_exit:
                            if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                                Input = Input[0:len(Input) - 1]
                            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                                if Input != "":
                                    if int(Input) == number:
                                        self.time = Timer.Timer()
                                        self.time.reset()
                                        self.correct = True
                                        self.answer_correct = True
                                    elif int(Input) > number:
                                        self.time = Timer.Timer()
                                        self.time.reset()
                                        self.big = True
                                    elif int(Input) < number:
                                        self.time = Timer.Timer()
                                        self.time.reset()
                                        self.small = True
                if self.number_exit:
                    self.Input = ""
                    if not self.bubble:
                        self.current_game = "Main"
                        self.first_loop = True
                        if self.answer_correct:
                            if self.player == "Orange Cat":
                                self.yellow_cat.lives = self.yellow_cat.lives + 1
                            else:
                                self.orange_cat.lives = self.orange_cat.lives + 1

                self.screen.fill((109, 255, 102))
                if self.correct:
                    self.create_text_bubble(["You did it!", "You are so lucky!", "+1 live!"], (225, 118), 5, "left")
                    self.number_exit = True
                elif self.big:
                    self.create_text_bubble(["The number you have", "entered is too big."], (225, 118), 5, "left")
                    self.number_exit = True
                elif self.small:
                    self.create_text_bubble(["The number you have", "entered is too small."], (225, 118), 5, "left")
                    self.number_exit = True
                if caret_timer.get_time() > 0.53:
                    if caret_display:
                        caret_display = False
                    else:
                        caret_display = True
                    caret_timer.reset()

                if self.player == "Orange Cat":
                    self.screen.blit(self.yellow_cat_img, (207, 48))
                else:
                    self.screen.blit(self.orange_cat_img, (241, 48))
                pygame.draw.rect(self.screen, (255, 255, 255), [280, 320, 160, 30], 0)
                self.screen.blit(self.font1.render("Guess a number between 1 and 100:",
                                                   True,
                                                   (0, 0, 0),
                                                   (109, 255, 102)),
                                 (12, 325))
                if caret_display:
                    pygame.draw.line(self.screen, (0, 0, 0), (286 + self.font1.size(Input)[0], 325),
                                     (286 + self.font1.size(Input)[0], 345), 1)
                self.screen.blit(self.font1.render(Input, True, (0, 0, 0), (255, 255, 255)), (285, 325))
                pygame.display.update()
            elif self.current_game == "Math":
                if self.first_loop:
                    Input = ""
                    self.number_exit = False
                    self.correct = False
                    self.answer_correct = False
                    self.answer_wrong = False
                    number1 = random.randint(0, 999)
                    number2 = random.randint(0, 999)
                    caret_display = True
                    caret_timer = Timer.Timer()
                    caret_timer.reset()
                    self.first_loop = False
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.gameRun = False
                        break
                    elif event.type == pygame.KEYDOWN:
                        if len(Input) <= 3:
                            if not self.number_exit:
                                if event.key == pygame.K_0 or event.key == pygame.K_KP0:
                                    Input = Input + "0"
                                elif event.key == pygame.K_1 or event.key == pygame.K_KP1:
                                    Input = Input + "1"
                                elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                                    Input = Input + "2"
                                elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                                    Input = Input + "3"
                                elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                                    Input = Input + "4"
                                elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
                                    Input = Input + "5"
                                elif event.key == pygame.K_6 or event.key == pygame.K_KP6:
                                    Input = Input + "6"
                                elif event.key == pygame.K_7 or event.key == pygame.K_KP7:
                                    Input = Input + "7"
                                elif event.key == pygame.K_8 or event.key == pygame.K_KP8:
                                    Input = Input + "8"
                                elif event.key == pygame.K_9 or event.key == pygame.K_KP9:
                                    Input = Input + "9"
                        if not self.number_exit:
                            if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                                Input = Input[0:len(Input) - 1]
                            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                                if Input != "":
                                    if int(Input) == number1 + number2:
                                        self.time = Timer.Timer()
                                        self.time.reset()
                                        self.correct = True
                                        self.answer_correct = True
                                    else:
                                        self.time = Timer.Timer()
                                        self.time.reset()
                                        self.answer_wrong = True
                if self.number_exit:
                    self.Input = ""
                    if not self.bubble:
                        self.current_game = "Main"
                        self.first_loop = True
                        if self.answer_wrong:
                            if self.player == "Orange Cat":
                                self.yellow_cat.lives = self.yellow_cat.lives - 1
                            else:
                                self.orange_cat.lives = self.orange_cat.lives - 1
                self.screen.fill((109, 255, 102))
                if self.correct:
                    self.create_text_bubble(["That is correct!"], (250, 118), 5, "right")
                    self.number_exit = True
                elif self.answer_wrong:
                    self.create_text_bubble(["That is wrong!", "The correct", "answer of",
                                             str(number1) + " + " + str(number2) + " is " + str(number1 + number2),
                                             "-1 life!"], (237, 118), 5, "right")
                    self.number_exit = True
                if caret_timer.get_time() > 0.53:
                    if caret_display:
                        caret_display = False
                    else:
                        caret_display = True
                    caret_timer.reset()

                if self.player == "Orange Cat":
                    self.screen.blit(self.yellow_cat_img, (317, 48))
                else:
                    self.screen.blit(self.orange_cat_img, (351, 48))
                pygame.draw.rect(self.screen, (255, 255, 255), [280, 320, 160, 30], 0)
                self.screen.blit(self.font1.render(str(number1) + " + " + str(number2) + " = ",
                                                   True,
                                                   (0, 0, 0),
                                                   (109, 255, 102)),
                                 (12, 325))
                if caret_display:
                    pygame.draw.line(self.screen, (0, 0, 0), (286 + self.font1.size(Input)[0], 325),
                                     (286 + self.font1.size(Input)[0], 345), 1)
                self.screen.blit(self.font1.render(Input, True, (0, 0, 0), (255, 255, 255)), (285, 325))
                pygame.display.update()
            elif self.current_game == "Maze":
                if self.player == "Orange Cat":
                    maze = Maze_Game.Maze(self.screen, "Yellow Cat", self.clock, self.yellow_cat.lives)
                else:
                    maze = Maze_Game.Maze(self.screen, "Orange Cat", self.clock, self.orange_cat.lives)
                if self.player == "Orange Cat":
                    self.yellow_cat.lives = maze.lives()
                else:
                    self.orange_cat.lives = maze.lives()
                if not maze.closed:
                    self.current_game = "Main"
                else:
                    self.gameRun = False

            elif self.current_game == "Fish":
                if self.player == "Orange Cat":
                    fish = Fish_Game.Main(self.screen, "Yellow Cat", self.clock)
                else:
                    fish = Fish_Game.Main(self.screen, "Orange Cat", self.clock)
                if fish.score_data() < 45:
                    if self.player == "Orange Cat":
                        self.yellow_cat.lives = self.yellow_cat.lives - 1
                    else:
                        self.orange_cat.lives = self.orange_cat.lives - 1
                if not fish.Exit:
                    self.current_game = "Main"
                else:
                    self.gameRun = False
            elif self.current_game == "Win":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.gameRun = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            self.first_loop = True
                            self.bubble = False
                            self.thread = None
                            self.run = True
                            self.trap1 = False
                            self.trap2 = False
                            self.max_width = 0
                            self.current_game = "Main"
                            self.dice = Dice.Dice()
                            self.orange_cat = Cat.Cat("Orange")
                            self.yellow_cat = Cat.Cat("Yellow")
                            self.steps = 0
                            self.player = "Orange Cat"
                            self.orange_cat.lives = 3
                            self.data = []
                            self.mode = ""
                            self.closed = False
                            self.trap1_init = True
                            self.trap2_init = True
                            self.gameRun = True
                            self.direction = ""
                self.screen.fill((255, 255, 255))
                if self.player == "Yellow Cat":
                    self.screen.blit(self.orange_cat_win_screen, (0, 0))
                else:
                    self.screen.blit(self.yellow_cat_win_screen, (0, 0))
                self.screen.blit(self.font1.render("Press the 'R' key to play again",
                                                   True,
                                                   (0, 0, 0),
                                                   (173, 110, 0)), (10, 330))
                pygame.display.update()
            elif self.current_game == "Lose":
                stop = False
                while self.lose_timer.get_time() <= 5:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.gameRun = False
                            stop = True
                    if stop:
                        break
                    self.screen.fill((255, 255, 255))
                    if self.player == "Yellow Cat":
                        self.screen.blit(self.yellow_cat_lose, (0, 0))
                    else:
                        self.screen.blit(self.orange_cat_lose, (0, 0))
                    pygame.display.update()
                self.current_game = "Win"
            elif self.current_game == "Instructions":
                pages = [
                    ["How to Play:",
                     "When you start the game, you will see a dice in the center of",
                     "the screen, eight squares on the screen, and two cats, one",
                     "orange, one yellow, on the first square. Then, you have to",
                     "find a friend to play with you. One of you will play as Orange",
                     "Cat, the other as Yellow Cat.",
                     "",
                     "On the top of the screen, you will see the sentence",
                     "'It is Orange Cat's turn to move'. Then, the person playing",
                     "as Orange Cat has to click the dice, and complete the game it",
                     "triggers. Once you complete the game, the sentence will change",
                     "to say 'It is Yellow Cat's turn to move'. Then the person who is",
                     "playing as Yellow Cat will click the dice and play the game it",
                     "triggers, etc. (Use the left and right arrow keys to navigate.)"],
                    ["Each cat has three lives, when one of the cats lose all his",
                     "lives, the player who's playing as the other cat wins! When",
                     "you click the dice, the cat who's turn has come will move",
                     "forward automatically. Stopping on each square will trigger a",
                     "different game.",
                     "",
                     "The player who's cat stops on the starting square after at least",
                     "one circle around the board wins!",
                     "",
                     "Stopping on the second square going clockwise",
                     "triggers a number guessing game. Enter a number between one",
                     "and a hundred and press enter. If you guess correctly you",
                     "will gain one life.",
                     "(Use the left and right arrow keys to navigate.)"],
                    ["The third square going clockwise triggers a math addition game.",
                     "Answer the question and press enter.",
                     "If you enter the wrong answer, you lose a life.",
                     "",
                     "The fourth square going clockwise triggers a maze game.",
                     "Click on the cat and it will start following your mouse cursor.",
                     "Guide it to the end of the maze without touching the walls.",
                     "There are different colored tripwires throughout. Some do",
                     "nothing, but some are fatal. If you have touched a tripwire",
                     "and been sent back to the start, try a different route.",
                     "",
                     "The fifth square going clockwise does nothing.",
                     "The sixth square going clockwise starts a fish catching game.",
                     "(Use the left and right arrow keys to navigate.)"],
                    ["Use the left and right arrow keys to control the",
                     "cat and catch as many fish as you can. The game",
                     "will end after one minute. If you have not caught",
                     "at least 45 fish by the time the game ends, you lose",
                     "a life.",
                     "",
                     "The seventh and eighth squares going clockwise are trap",
                     "squares that send you backwards.",
                     "(Press space to start)"]
                ]
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.gameRun = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            if self.page == len(pages) - 1:
                                self.current_game = "Main"
                        elif event.key == pygame.K_LEFT:
                            if self.page > 0:
                                self.page = self.page - 1
                        elif event.key == pygame.K_RIGHT:
                            if self.page < len(pages) - 1:
                                self.page = self.page + 1
                    self.screen.fill((109, 255, 102))
                    for line in range(0, len(pages[self.page])):
                        self.screen.blit(self.font1.render(pages[self.page][line],
                                                           True,
                                                           (0, 0, 0),
                                                           (109, 255, 102)), (10, 25 * line))
                    pygame.display.update()
        pygame.quit()

    def move_player(self):
        self.thread = threading.Thread(target=self.move)
        self.thread.start()

    def move(self):
        for i in range(0, 6):
            self.dice.costume = i
            time.sleep(0.5)
        self.dice.costume = self.dice.steps
        if self.player == "Orange Cat":
            for i in range(0, self.dice.steps):
                self.orange_cat.move()
                time.sleep(0.5)
        elif self.player == "Yellow Cat":
            for i in range(0, self.dice.steps):
                self.yellow_cat.move()
                time.sleep(0.5)
        if self.player == "Orange Cat":
            if self.orange_cat.pos_x == 131 and self.orange_cat.pos_y == 268.5 or self.orange_cat.pos_x == 131 and self.orange_cat.pos_y == 158.5:
                pass
            else:
                self.dice.active = True
        else:
            if self.yellow_cat.pos_x == 97 and self.yellow_cat.pos_y == 268.5 or self.yellow_cat.pos_x == 97 and self.yellow_cat.pos_y == 268.5:
                pass
            else:
                self.dice.active = True
        color = self.player
        if self.player == "Orange Cat":
            self.player = "Yellow Cat"
        else:
            self.player = "Orange Cat"
        self.start_game(color)

    def start_game(self, player):
        if player == "Orange Cat":
            if self.orange_cat.pos_x == 351 and self.orange_cat.pos_y == 158.5:
                self.current_game = "Maze"
            elif self.orange_cat.pos_x == 241 and self.orange_cat.pos_y == 48.5:
                self.current_game = "Number"
            elif self.orange_cat.pos_x == 351 and self.orange_cat.pos_y == 48.5:
                self.current_game = "Math"
            elif self.orange_cat.pos_x == 241 and self.orange_cat.pos_y == 268.5:
                self.current_game = "Fish"
            elif self.orange_cat.pos_x == 131 and self.orange_cat.pos_y == 268.5:
                self.trap1 = True
            elif self.orange_cat.pos_x == 131 and self.orange_cat.pos_y == 158.5:
                self.trap2 = True
            elif self.orange_cat.pos_x == 131 and self.orange_cat.pos_y == 48.5:
                self.current_game = "Win"
        else:
            if self.yellow_cat.pos_x == 317 and self.yellow_cat.pos_y == 158.5:
                self.current_game = "Maze"
            elif self.yellow_cat.pos_x == 207 and self.yellow_cat.pos_y == 48.5:
                self.current_game = "Number"
            elif self.yellow_cat.pos_x == 317 and self.yellow_cat.pos_y == 48.5:
                self.current_game = "Math"
            elif self.yellow_cat.pos_x == 207 and self.yellow_cat.pos_y == 268.5:
                self.current_game = "Fish"
            elif self.yellow_cat.pos_x == 97 and self.yellow_cat.pos_y == 268.5:
                self.trap1 = True
            elif self.yellow_cat.pos_x == 97 and self.yellow_cat.pos_y == 158.5:
                self.trap2 = True
            elif self.yellow_cat.pos_x == 97 and self.yellow_cat.pos_y == 48.5:
                self.current_game = "Win"

    def create_text_bubble(self, lines, location, seconds, direction):
        self.data.clear()
        self.data.append(lines)
        self.data.append(location)
        self.data.append(seconds)
        self.direction = direction
        if self.time.get_time() <= seconds:
            self.text_bubble()
        else:
            self.bubble = False
            self.big = False
            self.small = False
            self.correct = False

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
            pygame.draw.rect(self.screen, (255, 255, 255),
                             [self.location[0], self.location[1], self.max_width + 20, len(self.text) * 18], 0)
            pygame.draw.rect(self.screen, (255, 255, 255),
                             [self.location[0] + 10, self.location[1] - 10, self.max_width, len(self.text) * 18 + 20],
                             0)
            pygame.draw.circle(self.screen, (255, 255, 255), [self.location[0] + 10, self.location[1]], 10, 0)
            pygame.draw.circle(self.screen, (255, 255, 255), [self.location[0] + self.max_width + 10, self.location[1]],
                               10, 0)
            pygame.draw.circle(self.screen, (255, 255, 255),
                               [self.location[0] + 10, self.location[1] + len(self.text) * 18], 10, 0)
            pygame.draw.circle(self.screen, (255, 255, 255),
                               [self.location[0] + self.max_width + 10, self.location[1] + len(self.text) * 18], 10, 0)
            if self.direction == "left":
                pygame.draw.polygon(self.screen, (255, 255, 255), [(self.location[0] + 10, self.location[1]),
                                                                   (self.location[0] + 30, self.location[1]),
                                                                   (self.location[0] + 15, self.location[1] - 20)], 0)
            else:
                pygame.draw.polygon(self.screen, (255, 255, 255),
                                    [(self.location[0] + self.max_width - 10, self.location[1]),
                                     (self.location[0] + self.max_width - 30, self.location[1]),
                                     (self.location[0] + self.max_width - 15, self.location[1] - 20)], 0)
            for line in range(0, len(self.text)):
                self.screen.blit(self.text[line], self.text_locations[line])

    def square_trap(self, player):
        if self.trap1_timer.get_time() >= 1:
            if player == "Orange Cat":
                if self.orange_cat.pos_x == 351 and self.orange_cat.pos_y == 48.5:
                    self.trap1 = False
                    self.trap1_init = True
                    self.dice.active = True
                    self.start_game(player)
                elif self.orange_cat.pos_x == 131 and self.orange_cat.pos_y == 268.5:
                    self.orange_cat.pos_x = 241
                    self.orange_cat.pos_y = 268.5
                    self.orange_cat.direction = "left"
                elif self.orange_cat.pos_x == 241 and self.orange_cat.pos_y == 268.5:
                    self.orange_cat.pos_x = 351
                    self.orange_cat.pos_y = 268.5
                elif self.orange_cat.pos_x == 351 and self.orange_cat.pos_y == 268.5:
                    self.orange_cat.pos_y = 158.5
                    self.orange_cat.direction = "down"
                elif self.orange_cat.pos_x == 351 and self.orange_cat.pos_y == 158.5:
                    self.orange_cat.pos_y = 48.5
                self.trap1_timer.reset()
            else:
                if self.yellow_cat.pos_x == 317 and self.yellow_cat.pos_y == 48.5:
                    self.trap1 = False
                    self.trap1_init = True
                    self.dice.active = True
                    self.start_game(player)
                elif self.yellow_cat.pos_x == 97 and self.yellow_cat.pos_y == 268.5:
                    self.yellow_cat.pos_x = 207
                    self.yellow_cat.pos_y = 268.5
                    self.yellow_cat.direction = "left"
                elif self.yellow_cat.pos_x == 207 and self.yellow_cat.pos_y == 268.5:
                    self.yellow_cat.pos_x = 317
                    self.yellow_cat.pos_y = 268.5
                elif self.yellow_cat.pos_x == 317 and self.yellow_cat.pos_y == 268.5:
                    self.yellow_cat.pos_y = 158.5
                    self.yellow_cat.direction = "down"
                elif self.yellow_cat.pos_x == 317 and self.yellow_cat.pos_y == 158.5:
                    self.yellow_cat.pos_y = 48.5
                self.trap1_timer.reset()

    def square_trap2(self, player):
        if self.trap2_timer.get_time() >= 1:
            if player == "Orange Cat":
                if self.orange_cat.pos_x == 131 and self.orange_cat.pos_y == 268.5:
                    self.trap2 = False
                    self.trap2_init = True
                    self.start_game(player)
                else:
                    self.orange_cat.pos_y = 268.5
            else:
                if self.yellow_cat.pos_x == 97 and self.yellow_cat.pos_y == 268.5:
                    self.trap2 = False
                    self.trap2_init = True
                    self.start_game(player)
                else:
                    self.yellow_cat.pos_y = 268.5


if __name__ == "__main__":
    Main()
