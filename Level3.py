import pygame
import sys
import os
import pygame_gui
from Game_Over import GameOver
from Titles_show import Titles
from Pause import Pause


def level3(LANGUAGE, size, width, height):
    global isJump, jumpCount, x, fall, dead, run_away, show_titles, running, y
    SOUND_TITLES = True
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Level 3')
    screen.fill((0, 0, 0))
    FPS = 50
    clock = pygame.time.Clock()
    directory = os.path.join(os.getcwd(), 'data')
    achievements = []
    x, y = 500, 485

    def load_image(name, colorkey=None):
        fullname = os.path.join('data', name)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        return image

    walk_left = [load_image('R1.png'), load_image('R2.png'), load_image('R3.png'),
                load_image('R4.png'), load_image('R5.png'), load_image('R6.png'),
                load_image('R7.png'), load_image('R8.png'), load_image('R9.png'),
                load_image('R10.png')]
    walk_right = [pygame.transform.flip(load_image('R1.png'), 90, 0),
                 pygame.transform.flip(load_image('R2.png'), 90, 0),
                 pygame.transform.flip(load_image('R3.png'), 90, 0),
                 pygame.transform.flip(load_image('R4.png'), 90, 0),
                 pygame.transform.flip(load_image('R5.png'), 90, 0),
                 pygame.transform.flip(load_image('R6.png'), 90, 0),
                 pygame.transform.flip(load_image('R7.png'), 90, 0),
                 pygame.transform.flip(load_image('R8.png'), 90, 0),
                 pygame.transform.flip(load_image('R9.png'), 90, 0),
                 pygame.transform.flip(load_image('R10.png'), 90, 0)]
    jump_left = [load_image('J1.png'), load_image('J2.png'), load_image('J3.png'),
                load_image('J4.png'), load_image('J5.png'), load_image('J6.png'),
                load_image('J7.png'), load_image('J8.png'), load_image('J9.png'),
                load_image('J10.png')]
    jump_right = [pygame.transform.flip(load_image('J1.png'), 90, 0),
                 pygame.transform.flip(load_image('J2.png'), 90, 0),
                 pygame.transform.flip(load_image('J3.png'), 90, 0),
                 pygame.transform.flip(load_image('J4.png'), 90, 0),
                 pygame.transform.flip(load_image('J5.png'), 90, 0),
                 pygame.transform.flip(load_image('J6.png'), 90, 0),
                 pygame.transform.flip(load_image('J7.png'), 90, 0),
                 pygame.transform.flip(load_image('J8.png'), 90, 0),
                 pygame.transform.flip(load_image('J9.png'), 90, 0),
                 pygame.transform.flip(load_image('J10.png'), 90, 0)]
    enemy_walk = [pygame.transform.scale(load_image('demon_walk_1.png'), (400, 300)),
                  pygame.transform.scale(load_image('demon_walk_2.png'), (400, 300)),
                  pygame.transform.scale(load_image('demon_walk_3.png'), (400, 300)),
                  pygame.transform.scale(load_image('demon_walk_4.png'), (400, 300)),
                  pygame.transform.scale(load_image('demon_walk_5.png'), (400, 300)),
                  pygame.transform.scale(load_image('demon_walk_6.png'), (400, 300)),
                  pygame.transform.scale(load_image('demon_walk_7.png'), (400, 300)),
                  pygame.transform.scale(load_image('demon_walk_8.png'), (400, 300)),
                  pygame.transform.scale(load_image('demon_walk_9.png'), (400, 300)),
                  pygame.transform.scale(load_image('demon_walk_10.png'), (400, 300)),
                  pygame.transform.scale(load_image('demon_walk_11.png'), (400, 300)),
                  pygame.transform.scale(load_image('demon_walk_12.png'), (400, 300))]
    bg = load_image('bg.jpg')

    isJump = False
    jumpCount = 10
    fall = False

    class Hero(pygame.sprite.Sprite):
        def __init__(self, x, y, where, *group):
            super().__init__(*group)
            self.i = 0
            self.where = where
            if where == 'right':
                self.image = pygame.transform.scale(walk_right[0], (100, 100))
            else:
                self.image = pygame.transform.scale(walk_left[0], (100, 100))
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.k = 4
            self.foot = 5

        def update(self, where, move=True):
            global isJump, jumpCount, x, fall, dead, run_away, show_titles, running
            x_new = x
            fall = True
            for sprite in pads:
                if pygame.sprite.collide_mask(self, sprite):
                    fall = sprite.rect.y - sprite.rect.height / 2 <= self.rect.y <= \
                           sprite.rect.y + sprite.rect.height
                    if fall:
                        self.rect.y += 4
            if fall and not isJump:
                isJump = True
                jumpCount = -1
            if not fall and jumpCount <= 0:
                isJump = False
                jumpCount = 10
            if not isJump:
                if move:
                    self.i += 1
                    self.i = self.i % len(walk_right)
                    if self.where != where:
                        self.i = 0
                        self.where = where
                    if where == 'right':
                        self.image = pygame.transform.scale(walk_right[self.i], (100, 100))
                        x_new += self.foot
                    else:
                        self.image = pygame.transform.scale(walk_left[self.i], (100, 100))
                        x_new -= self.foot
                else:
                    self.i = 0
                    if where == 'right':
                        self.image = pygame.transform.scale(walk_right[self.i], (100, 100))
                    else:
                        self.image = pygame.transform.scale(walk_left[self.i], (100, 100))
            else:
                if jumpCount >= -10 or fall:
                    jumpCount -= 0.5
                    self.i += 1
                    y_down = 0
                    self.i = self.i % len(walk_right)
                    if move:
                        if where == 'right':
                            self.image = pygame.transform.scale(jump_right[self.i], (100, 100))
                            y_down -= jumpCount * self.k
                            x_new += self.foot
                        else:
                            self.image = pygame.transform.scale(jump_left[self.i], (100, 100))
                            y_down -= jumpCount * self.k
                            x_new -= self.foot
                    else:
                        if where == 'right':
                            self.image = pygame.transform.scale(jump_right[self.i], (100, 100))
                        else:
                            self.image = pygame.transform.scale(jump_left[self.i], (100, 100))
                        y_down -= jumpCount * self.k
                    y_down = int(y_down)
                    if y_down < 0:
                        end = 0
                        while y_down != 0:
                            self.rect.y -= 1
                            y_down += 1
                            for sprite in pads:
                                if pygame.sprite.collide_mask(self, sprite):
                                    if sprite.rect.y - sprite.rect.height / 2 <= self.rect.y <= \
                                            sprite.rect.y + sprite.rect.height:
                                        jumpCount = -1
                                        end = 1
                                        break
                                    else:
                                        jumpCount = 10
                                        isJump = False
                                        y_down = 0
                                        self.i = 0
                                        break
                            if end == 1:
                                break
                    else:
                        end = 0
                        while y_down != 0:
                            self.rect.y += 1
                            y_down -= 1
                            for sprite in pads:
                                if pygame.sprite.collide_mask(self, sprite):
                                    if sprite.rect.y - sprite.rect.height / 2 <= self.rect.y <= \
                                            sprite.rect.y + sprite.rect.height:
                                        jumpCount = -1
                                        end = 1
                                        break
                                    else:
                                        jumpCount = 10
                                        isJump = False
                                        y_down = 0
                                        self.i = 0
                                        break
                            if end == 1:
                                break
                else:
                    jumpCount = 10
                    isJump = False
                    self.i = 0
            self.mask = pygame.mask.from_surface(self.image)
            if not run_away and x_new < -645:
                x_new = -645
            if run_away and x_new < -670 and self.rect.y >= 550:
                sea.stop()
                splash.play()
                screen.fill((0, 0, 0))
                pygame.display.flip()
                clock.tick(0.5)
                get_achievement.play()
                return 3, achievements
            for sprite in enemies:
                if pygame.sprite.collide_mask(self, sprite):
                    dead = True
                    if self.rect.y < -50:
                        achievements.append('Вне границ')
                        get_achievement.play()
            if self.rect.y >= 650:
                dead = True
            if (500 <= x_new <= 600 and not first_titles_shown) or \
                    (x_new >= 9100 and not second_titles_shown and not isJump) or \
                    (500 <= x_new <= 600 and not isJump and not third_titles_shown and run_away):
                show_titles = True
            return x_new, self.rect.y

        def stay(self):
            self.i = 0
            if self.where == 'right':
                self.image = pygame.transform.scale(walk_right[self.i], (100, 100))
            else:
                self.image = pygame.transform.scale(walk_left[self.i], (100, 100))

        def change_jump(self):
            global isJump
            isJump = not isJump
            self.i = 0

    class Pad(pygame.sprite.Sprite):
        image = pygame.transform.scale(load_image('Pad_3_3.png'), (415, 65))
        image1 = pygame.transform.scale(load_image('Pad_3_3.png'), (350, 80))

        def __init__(self, place, y, type):
            super().__init__(all_sprites)
            if type == 1:
                self.image = Pad.image
            else:
                self.image = Pad.image1
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.rect.x = 1000
            self.rect.y = y
            self.add(pads)
            self.place = place

        def update(self):
            global x, y
            # Для расположения менять здесь
            self.rect.x = self.place - x

    class Sea(pygame.sprite.Sprite):
        image = load_image('sea.png')

        def __init__(self):
            super().__init__(all_sprites)
            self.image = Sea.image
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.rect.x = 1000
            self.rect.y = 560
            self.add(static_objects)
            self.sound = pygame.mixer.Sound(os.path.join(directory, 'WindySea.wav'))
            self.play = False

        def update(self):
            global x, y
            # Для расположения менять здесь
            self.rect.x = -1200 - x
            if self.rect.x > -980:
                if not self.play:
                    self.sound.play(-1)
                    self.play = True
            else:
                self.sound.stop()
                self.play = False

        def stop(self):
            self.sound.stop()
            self.play = False

    class Enemy(pygame.sprite.Sprite):

        def __init__(self, start, end, y):
            super().__init__(all_sprites)
            self.i = 0
            self.place_x = start
            self.move = 'right'
            self.image = pygame.transform.flip(enemy_walk[self.i], 90, 0)
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.rect.y = y
            self.start = start
            self.end = end
            self.add(enemies)
            self.foot = 4

        def update(self):
            global x
            self.i += 1
            self.i %= len(enemy_walk)
            if self.place_x > self.end:
                self.move = 'left'
                self.i = 0
            elif self.place_x < self.start:
                self.move = 'right'
                self.i = 0
            if self.move == 'right':
                self.image = pygame.transform.flip(enemy_walk[self.i], 90, 0)
                self.place_x += self.foot
            else:
                self.image = enemy_walk[self.i]
                self.place_x -= self.foot
            self.mask = pygame.mask.from_surface(self.image)
            self.rect.x = self.place_x - x

    class Pursuit(pygame.sprite.Sprite):
        def __init__(self, start, end, y, y_up):
            super().__init__(all_sprites)
            self.frames_run = cut_sheet(load_image('Run.png'), 1, 6)
            self.frames_attack = cut_sheet(load_image('All Attacks.png'), 1, 29)
            self.i = 0
            self.place_x = end
            self.move = 'left'
            self.image = pygame.transform.scale(pygame.transform.flip(
                enemy_walk[self.i], 90, 0), (200, 300))
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.rect.y = y
            self.start = start
            self.end = end
            self.add(enemies)
            self.foot = 6
            self.y_up = y_up
            self.attack = False

        def update(self):
            global x, y
            if not self.attack:
                if self.start - 450 <= x <= self.end - 555 and y > self.y_up:
                    if self.move == 'left':
                        near = 0 <= abs(abs(self.place_x - x) - 300) - 20 <= 50
                    else:
                        near = 0 <= abs(self.place_x - x) <= 50
                    if near:
                        if self.place_x < x:
                            self.move = 'left'
                        else:
                            self.move = 'right'
                        self.attack = True
                        self.i = 0
                    else:
                        self.i += 1
                        self.i %= len(self.frames_run)
                        if self.place_x < x and self.move != 'right':
                            self.move = 'right'
                            self.i = 0
                        elif self.place_x > x and self.move != 'left':
                            self.move = 'left'
                            self.i = 0
                        if self.move == 'left':
                            self.image = pygame.transform.scale(pygame.transform.flip(
                                self.frames_run[self.i], 90, 0), (300, 300))
                            self.place_x -= self.foot
                        else:
                            self.image = pygame.transform.scale(self.frames_run[self.i], (300, 300))
                            self.place_x += self.foot
                else:
                    self.i += 1
                    self.i %= len(self.frames_run)
                    if self.place_x > self.end:
                        self.move = 'left'
                        self.i = 0
                    elif self.place_x < self.start:
                        self.move = 'right'
                        self.i = 0
                    if self.move == 'left':
                        self.image = pygame.transform.scale(pygame.transform.flip(
                            self.frames_run[self.i], 90, 0), (300, 300))
                        self.place_x -= self.foot
                    else:
                        self.image = pygame.transform.scale(self.frames_run[self.i], (300, 300))
                        self.place_x += self.foot
            else:
                self.i += 1
                if self.move == 'left':
                    self.image = pygame.transform.scale(pygame.transform.flip(
                        self.frames_attack[self.i], 90, 0), (300, 300))
                else:
                    self.image = pygame.transform.scale(self.frames_attack[self.i], (300, 300))
                if self.i + 1 >= len(self.frames_attack):
                    self.attack = False
            self.mask = pygame.mask.from_surface(self.image)
            self.rect.x = self.place_x - x

    def cut_sheet(sheet, columns, rows):
        rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                           sheet.get_height() // rows)
        frames = []
        for j in range(rows):
            for i in range(columns):
                frame_location = (rect.w * i, rect.h * j)
                frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, rect.size)))
        return frames

    class RunningShootingGuy(pygame.sprite.Sprite):
        def __init__(self, start, end, y, points):
            super().__init__(all_sprites)
            self.frames_run = cut_sheet(load_image('Sci-fi Samurai Bandit-Spritet.png'), 6, 6)[:12]
            self.frames_attack = cut_sheet(load_image('blood explosion gun spell-Sheet.png'), 1, 19)
            self.i = 0
            self.place_x = end
            self.move = 'left'
            self.image = pygame.transform.scale(
                pygame.transform.flip(self.frames_run[self.i], 90, 0),
                (300, 300))
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.rect.y = y
            self.start = start
            self.end = end
            self.add(enemies)
            self.foot = 4
            self.points = points
            self.next = self.points[-1]
            self.i_next = -1
            self.shoot = False
            self.were = [0]

        def update(self):
            if self.move == 'right':
                rule = self.next - self.foot <= self.place_x <= self.next + self.foot
            else:
                rule = self.next - self.foot <= self.place_x + 300 <= self.next + self.foot
            if rule:
                self.shoot = True
                if self.move == 'left':
                    self.i_next -= 1
                    if abs(self.i_next) > len(self.points):
                        self.i_next = -1
                    self.place_x -= 800
                else:
                    self.i_next += 1
                    if self.i_next >= len(self.points):
                        self.i_next = 0
                self.next = self.points[self.i_next]
                self.i = 0
            if self.shoot:
                tm = pygame.time.get_ticks() // 100
                if tm not in self.were:
                    self.i += 1
                    if self.i >= len(self.frames_attack):
                        self.shoot = False
                        if self.move == 'left':
                            self.place_x += 800
                    else:
                        if self.move == 'left':
                            self.image = pygame.transform.scale(
                                pygame.transform.flip(self.frames_attack[self.i], 90, 0),
                                (1200, 300))
                        else:
                            self.image = pygame.transform.scale(self.frames_attack[self.i],
                                                                (1200, 300))
                    del self.were[-1]
                    self.were.append(tm)
            if not self.shoot:
                self.i += 1
                self.i %= len(self.frames_run)
                if self.place_x > self.end:
                    self.move = 'left'
                    self.i = 0
                    self.i_next = -1
                    self.next = self.points[self.i_next]
                elif self.place_x < self.start:
                    self.move = 'right'
                    self.i = 0
                    self.i_next = 0
                    self.next = self.points[self.i_next]
                if self.move == 'left':
                    self.image = pygame.transform.scale(
                        pygame.transform.flip(self.frames_run[self.i], 90, 0), (300, 300))
                    self.place_x -= self.foot
                else:
                    self.image = pygame.transform.scale(self.frames_run[self.i], (300, 300))
                    self.place_x += self.foot
            self.mask = pygame.mask.from_surface(self.image)
            self.rect.x = self.place_x - x

    class WaitBomb(pygame.sprite.Sprite):
        def __init__(self, place_x, y):
            super().__init__(all_sprites)
            self.frames_stay = cut_sheet(load_image('Idle.png'), 1, 4)
            self.frames_attack = cut_sheet(load_image('Attack.png'), 1, 9)
            self.i = 0
            self.place_x = place_x
            self.image = pygame.transform.scale(self.frames_stay[self.i], (400, 300))
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.rect.y = y
            self.add(enemies)
            self.shoot = False
            self.were = [0]
            self.pause = 0

        def update(self):
            if 80 <= self.rect.x <= 680 and not self.shoot:
                self.i = 0
                self.shoot = True
            tm = pygame.time.get_ticks() // 200
            if tm not in self.were:
                if not self.shoot and not self.pause:
                    self.i += 1
                    self.i %= len(self.frames_stay)
                    self.image = pygame.transform.scale(self.frames_stay[self.i], (400, 300))
                elif self.pause:
                    self.i = 0
                    self.image = pygame.transform.scale(self.frames_stay[self.i], (400, 300))
                    self.pause -= 1
                else:
                    self.i += 1
                    self.image = pygame.transform.scale(self.frames_attack[self.i], (600, 300))
                    if self.i + 1 >= len(self.frames_attack):
                        self.i = 0
                        self.shoot = False
                        self.pause = 15
                del self.were[-1]
                self.were.append(tm)
            self.mask = pygame.mask.from_surface(self.image)
            self.rect.x = self.place_x - x

    class AnimatedSprite(pygame.sprite.Sprite):
        def __init__(self, sheet, columns, rows, x, y, size, mirror=False, ps=False):
            super().__init__(all_sprites)
            self.frames = []
            self.cut_sheet(sheet, columns, rows)
            self.cur_frame = 0
            self.image = self.frames[self.cur_frame]
            self.mask = pygame.mask.from_surface(self.image)
            self.rect.move(x, y)
            self.place_x = x
            self.rect.y = y
            self.add(static_objects)
            self.size = size
            self.were = [0]
            if mirror:
                new_frames = self.frames.copy()
                for elem in self.frames:
                    new_frames.append(pygame.transform.flip(elem, 90, 0))
                self.frames = new_frames.copy()
            self.ps = ps
            self.stopped = 0

        def cut_sheet(self, sheet, columns, rows):
            self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                    sheet.get_height() // rows)
            for j in range(rows):
                for i in range(columns):
                    frame_location = (self.rect.w * i, self.rect.h * j)
                    self.frames.append(sheet.subsurface(pygame.Rect(
                        frame_location, self.rect.size)))

        def update(self):
            global x
            tm = pygame.time.get_ticks() // 100
            if tm not in self.were:
                if self.ps and (self.cur_frame + 1) % len(self.frames) == 1 and self.stopped < 15:
                    self.cur_frame -= 1
                    self.stopped += 1
                else:
                    self.stopped = 0
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                self.image = pygame.transform.scale(self.frames[self.cur_frame], self.size)
                del self.were[-1]
                self.were.append(tm)
            self.mask = pygame.mask.from_surface(self.image)
            # Для расположения менять здесь
            self.rect.x = self.place_x - x

    class BlackSquare(pygame.sprite.Sprite):
        def __init__(self, size_x, size_y, pos):
            super().__init__(all_sprites)
            self.size_x = size_x
            self.size_y = size_y
            self.place_x = pos[0]
            self.image = pygame.Surface((size_x, size_y),
                                        pygame.SRCALPHA, 32)
            pygame.draw.rect(self.image, pygame.Color("black"), (0, 0, size_x, size_y))
            self.rect = pygame.Rect(self.place_x, -100, size_x, size_y)
            self.mask = pygame.mask.from_surface(self.image)
            self.add(enemies)
            self.foot = 1.9

        def update(self):
            global x
            if run_away:
                self.size_x += self.foot
                self.place_x -= self.foot
                self.image = pygame.Surface((self.size_x, self.size_y),
                                            pygame.SRCALPHA, 32)
                pygame.draw.rect(self.image, pygame.Color("black"),
                                 (0, 0, self.size_x, self.size_y))
                self.rect = pygame.Rect(self.place_x - x, -100, self.size_x, self.size_y)
                self.mask = pygame.mask.from_surface(self.image)

    all_sprites = pygame.sprite.Group()
    pads = pygame.sprite.Group()
    static_objects = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    Enemy(-80, 215, 105)
    Enemy(1620, 1900, -145)
    Enemy(3850, 4110, 205)
    sea = Sea()
    start = -100
    for i in range(4):
        Pad(start + i * 415, 590, 1)
    for i in range(3):
        Pad(2400 + i * 325, 500, 2)
    Pad(1400, 400, 2)
    Pad(100, 400, 2)
    Pad(1800, 150, 2)
    Pad(1700, 600, 2)
    Pad(2100, 450, 2)
    Pad(3200, 250, 2)
    Pad(3600, 400, 1)
    Pad(4000, 500, 2)
    for i in range(15):
        Pad(4300 + i * 340, 600, 2)
    for i in range(4):
        Pad(4810 + i * 1400, 350, 2)
    Pad(9500, 450, 2)

    jump_where = 'right'
    hero = Hero(x, y, jump_where, all_sprites)
    dead = False
    pause = False
    run_away = False
    running = True
    showed_death = False
    show_titles = False
    pressed_enter = False
    end_screen = GameOver(width, height)
    pause_screen = Pause(width, height)
    manager_game_over = pygame_gui.UIManager((width, height))
    manager_pause = pygame_gui.UIManager((width, height))
    game_over_sound = pygame.mixer.Sound(os.path.join(directory, 'Game over.mp3'))
    splash = pygame.mixer.Sound(os.path.join(directory, 'Jumping into water.mp3'))
    typing = pygame.mixer.Sound(os.path.join(directory, 'Typing.mp3'))
    end_typing = pygame.mixer.Sound(os.path.join(directory, 'End typing.mp3'))
    get_achievement = pygame.mixer.Sound(os.path.join(directory, 'Achievement.wav'))
    game_over_sound.set_volume(3)
    Pursuit(4300, 9100, 350, 300)
    RunningShootingGuy(4300, 9400, 350, [4300, 5000, 5700, 6400, 7100, 8800, 9400])
    for i in range(3):
        WaitBomb(5600 + i * 1350, 380)
    BlackSquare(1000, 1000, (9700, -100))
    portal = AnimatedSprite(load_image("Purple Portal Sprite Sheet.png"), 8, 1, 800, 350,
                            (300, 300))
    drone_portal = AnimatedSprite(load_image('Guardian Sprite-Sheet.png'), 1, 39, 1710, 480,
                                  (350, 200), True)
    drone_portal1 = AnimatedSprite(load_image('Guardian Sprite-Sheet.png'), 1, 39, 3600, 280,
                                   (350, 200), True)
    shooter = AnimatedSprite(
        pygame.transform.flip(load_image('blood explosion gun spell-Sheet.png'),
                              90, 0), 1, 19, 2300, 300, (1200, 300), ps=True)
    drone_portal.add(enemies)
    drone_portal1.add(enemies)
    shooter.add(enemies)
    first_titles = Titles(
        '[Главный герой:] Где это я?|| И что с моим телом?£ '
        '[Смерть:] Ты в магическом мире, это последнее испытание.| &Я перенес тебя в другое тело, так '
        'как твое слишком дряхлое.£ '
        '[Главный герой:] Хорошо, нужно будет занятся спортом.| Еще чуть-чуть и я смогу вернуться.£ '
        '[Смерть:] Опасайся монстров, они убьют тебя без раздумий и меч тут не поможет.£ ' * (
                LANGUAGE == 'Русский') +
        "[Main hero:] Where am I? What's with my body?£ "
        "[Death:] You're in the magic world. It's your last trial.| &I transferred you to another body "
        "because yours is too decrepit.£ "
        "[Main hero:] Ok, I'll need to do some sports after return.| Just a little more and I can come "
        "back.£ "
        "[Death:] Be careful, monsters can easily kill you and your sword won't help you.£ " * (
                LANGUAGE == 'English'), width, height,
        os.path.join(directory, 'CinecavXSans-Regular.ttf'))
    first_titles_shown = False
    second_titles = Titles(
        '[Главный герой:] И куда теперь?£ '
        '[Смерть:] Хм|.|.|.| Все должно было быть по другому£ '
        '[Неизвестный голос:] Ты отсюда никогда не выберешься!| &Ты не заботился о своих близких и '
        'думал только о себе!£ '
        '[Смерть:] Что-то надвигается, беги обратно в портал!£ ' * (
                LANGUAGE == 'Русский') +
        "[Main hero:] So where should I go?£ "
        "[Death:] Hmm|.|.|.| Everything should have been different£ "
        "[Unknown:] You'll never get out!| &You didn't care about your loved ones and thought only "
        "about yourself!£ "
        "[Death:] Something is happening, run back to the portal!£ " * (
                LANGUAGE == 'English'), width, height,
        os.path.join(directory, 'CinecavXSans-Regular.ttf'))
    second_titles_shown = False
    third_titles = Titles(
        '[Главный герой:] Я не могу зайти в портал!£ '
        '[Смерть:] Я не могу ничего с этим сделать!| Видимо, придется прыгать в воду.£ ' * (
                LANGUAGE == 'Русский') +
        "[Main hero:] I can't enter the portal!£ "
        "[Death:] I can do nothing!| Apparently, you'll have to jump into water.£ " * (
                LANGUAGE == 'English'), width, height,
        os.path.join(directory, 'CinecavXSans-Regular.ttf'))
    third_titles_shown = False
    button_back_main_window = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((400, 355, 200, 50)),
        text='На главный экран' * (LANGUAGE == 'Русский') + 'Main Window' * (LANGUAGE == 'English'),
        manager=manager_game_over
    )
    button_last_save = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((400, 300, 200, 50)),
        text='К последнему сохранению' * (LANGUAGE == 'Русский') + 'Last checkpoint' * (
                LANGUAGE == 'English'),
        manager=manager_game_over
    )

    button_back_main_window_pause = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((25, 575, 200, 50)),
        text='На главный экран' * (LANGUAGE == 'Русский') + 'Main Window' * (LANGUAGE == 'English'),
        manager=manager_pause
    )
    button_last_save_pause = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((400, 270, 200, 50)),
        text='К последнему сохранению' * (LANGUAGE == 'Русский') + 'Last checkpoint' * (
                LANGUAGE == 'English'),
        manager=manager_pause
    )
    if SOUND_TITLES:
        button_sound_titles = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((775, 575, 200, 50)),
            text='Звук титров: включён' * (LANGUAGE == 'Русский') + 'Caption sound: on' * (
                    LANGUAGE == 'English'),
            manager=manager_pause
        )
    else:
        button_sound_titles = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((775, 575, 200, 50)),
            text='Звук титров: выключен' * (LANGUAGE == 'Русский') + 'Caption sound: off' * (
                    LANGUAGE == 'English'),
            manager=manager_pause
        )
    while running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and
                                             event.key == pygame.K_ESCAPE):
                pause = not pause
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                pressed_enter = True
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element in (
                            button_back_main_window, button_back_main_window_pause):
                        return 0, achievements
                    elif event.ui_element in (button_last_save, button_last_save_pause):
                        return 1, achievements
                    if event.ui_element == button_sound_titles:
                        SOUND_TITLES = not SOUND_TITLES
                        button_sound_titles.kill()
                        if SOUND_TITLES:
                            button_sound_titles = pygame_gui.elements.UIButton(
                                relative_rect=pygame.Rect((775, 575, 200, 50)),
                                text='Звук титров: включён' * (
                                        LANGUAGE == 'Русский') + 'Caption sound: on' * (
                                             LANGUAGE == 'English'),
                                manager=manager_pause
                            )
                        else:
                            button_sound_titles = pygame_gui.elements.UIButton(
                                relative_rect=pygame.Rect((775, 575, 200, 50)),
                                text='Звук титров: выключен' * (
                                        LANGUAGE == 'Русский') + 'Caption sound: off' * (
                                             LANGUAGE == 'English'),
                                manager=manager_pause
                            )
            manager_game_over.process_events(event)
            manager_pause.process_events(event)
        if dead:
            if not showed_death:
                sea.stop()
                game_over_sound.play()
                clock.tick(0.5)
                showed_death = True
            end_screen.update(time_delta, screen, manager_game_over)
        elif pause:
            sea.stop()
            for elem in [first_titles, second_titles]:
                elem.pause(typing, end_typing)
            pause_screen.update(time_delta, screen, manager_pause)
        else:
            if not show_titles:
                keys = pygame.key.get_pressed()
                if not isJump and keys[pygame.K_SPACE]:
                    hero.change_jump()
                if keys[pygame.K_LEFT]:
                    jump_where = 'left'
                    x, y = hero.update(jump_where)
                elif keys[pygame.K_RIGHT]:
                    jump_where = 'right'
                    x, y = hero.update(jump_where)
                else:
                    x, y = hero.update(jump_where, move=False)
                for sprite in pads:
                    sprite.update()
                for sprite in static_objects:
                    sprite.update()
                for sprite in enemies:
                    sprite.update()
                screen.fill('black')
                screen.blit(bg, (0, 0))
                all_sprites.draw(screen)
            else:
                x, y = hero.update(jump_where, move=False)
                screen.fill('black')
                screen.blit(bg, (0, 0))
                all_sprites.draw(screen)
                if 500 <= x <= 600 and not first_titles_shown:
                    if SOUND_TITLES:
                        first_titles_shown, pressed_enter = first_titles.update(screen, clock,
                                                                                pressed_enter,
                                                                                'black',
                                                                                typing,
                                                                                end_typing)
                    else:
                        first_titles_shown, pressed_enter = first_titles.update(screen, clock,
                                                                                pressed_enter,
                                                                                'black')
                    if first_titles_shown:
                        show_titles = False
                        pressed_enter = False
                if x >= 9100 and not second_titles_shown and not isJump:
                    if SOUND_TITLES:
                        second_titles_shown, pressed_enter = second_titles.update(screen, clock,
                                                                                  pressed_enter,
                                                                                  'black',
                                                                                  typing,
                                                                                  end_typing)
                    else:
                        second_titles_shown, pressed_enter = second_titles.update(screen, clock,
                                                                                  pressed_enter,
                                                                                  'black')
                    if second_titles_shown:
                        show_titles = False
                        pressed_enter = False
                        run_away = True
                if 500 <= x <= 600 and not isJump and not third_titles_shown and run_away:
                    if SOUND_TITLES:
                        third_titles_shown, pressed_enter = third_titles.update(screen, clock,
                                                                                pressed_enter,
                                                                                'black',
                                                                                typing,
                                                                                end_typing)
                    else:
                        third_titles_shown, pressed_enter = third_titles.update(screen, clock,
                                                                                pressed_enter,
                                                                                'black')
                    if third_titles_shown:
                        show_titles = False
                        pressed_enter = False
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()