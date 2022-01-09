from math import pi, cos, sin
from random import choice, uniform, randrange
from random import randint
import pygame
import os
import sys


pygame.init()
size = width, height = 1200, 800
screen = pygame.display.set_mode(size)
screen.fill((0, 0, 0))
clock = pygame.time.Clock()
FPS = 10


vec2, vec3 = pygame.math.Vector2, pygame.math.Vector3
NUMBER = 2000
CENTER = vec2(width // 2, height // 2)
Z = 140
ANGLE = 30
transfer = True
k5 = 0
all_sprites = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл не найден")
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


class Star:
    def __init__(self):
        self.pos3d = self.get_pos3d()
        self.s = uniform(0.45, 0.95)
        self.color = choice([(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255)])
        self.screen_pos = vec2(0, 0)
        self.size = 10

    def get_pos3d(self, scale_pos=35):
        angle = uniform(0, 2 * pi)
        radius = randrange(height // 4, height // 3) * scale_pos
        x = radius * cos(angle)
        y = radius * sin(angle)
        return vec3(x, y, Z)

    def update(self):
        self.pos3d.z -= self.s
        if self.pos3d.z < 1:
            self.pos3d = self.get_pos3d()
        self.screen_pos = vec2(self.pos3d.x, self.pos3d.y) / self.pos3d.z + CENTER
        self.size = (Z - self.pos3d.z) / (0.2 * self.pos3d.z)
        self.pos3d.xy = self.pos3d.xy.rotate(0.2)

    def draw(self):
        s = self.size
        if -s < self.screen_pos.x < width + s and -s < self.screen_pos.y < height + s:
            pygame.draw.rect(screen, self.color, (*self.screen_pos, self.size, self.size))


class StarField:
    def __init__(self):
        self.stars = [Star() for i in range(NUMBER)]

    def run(self):
        [i.update() for i in self.stars]
        [i.draw() for i in self.stars]


starfield = StarField()
while transfer:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            transfer = False
    if k5 == 500:
        k5 = 0
        transfer = False
    k5 += 1
    screen.fill((0, 0, 0))
    starfield.run()
    pygame.display.flip()
    clock.tick(60)
screen.fill((0, 0, 0))


def start_window(width, height):
    background = pygame.transform.scale(load_image("startpicture.png"), (width, height))
    screen.blit(background, (0, 0))
    button = pygame.transform.scale(load_image("button.png"), (450, 200))
    screen.blit(button, (375, 300))
    font = pygame.font.Font(None, 100)
    text = font.render("Начать игру", True, (255, 255, 255))
    text_x = width // 2 - text.get_width() // 2
    text_y = height // 2 - text.get_height() // 2
    screen.blit(text, (text_x, text_y))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 375 <= event.pos[0] <= 825 and 300 <= event.pos[1] <= 500:
                    return
        pygame.display.flip()
        clock.tick(FPS)


class Floor(pygame.sprite.Sprite):
    image = load_image("floor.png")

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Floor.image
        self.image = pygame.transform.scale(self.image, (1200, 300))
        self.rect = self.image.get_rect()
        self.rect.bottom = height


class FloorUp(pygame.sprite.Sprite):
    image = load_image("middle.png")

    def __init__(self, x):
        super().__init__(all_sprites)
        self.image = FloorUp.image
        self.image = pygame.transform.scale(self.image, (400, 110))
        self.rect = self.image.get_rect()
        self.rect.top = 390
        self.rect.x = x


class Background(pygame.sprite.Sprite):
    image = load_image("stone1.png")

    def __init__(self, x):
        super().__init__(all_sprites)
        self.image = Background.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = 400


class Run(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__(all_sprites)
        self.image = image
        self.image = pygame.transform.scale(self.image, (180, 230))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(300, 275)


class Start(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__(all_sprites)
        self.image = image
        self.image = pygame.transform.scale(self.image, (180, 230))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(300, 275)


class Jump(pygame.sprite.Sprite):
    def __init__(self, image, y):
        super().__init__(all_sprites)
        self.image = image
        self.image = pygame.transform.scale(self.image, (180, 230))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(300, y)


class Subject(pygame.sprite.Sprite):
    def __init__(self, name, image, x):
        super().__init__(all_sprites)
        self.image = image
        if name == "stone":
            self.image = pygame.transform.scale(self.image, (180, 100))
            self.rect = self.image.get_rect()
            self.rect = self.rect.move(x, 410)
        elif name == "boots":
            self.image = pygame.transform.scale(self.image, (180, 200))
            self.rect = self.image.get_rect()
            self.rect = self.rect.move(x, 360)
        elif name == "bag":
            self.image = pygame.transform.scale(self.image, (200, 200))
            self.rect = self.image.get_rect()
            self.rect = self.rect.move(x, 360)
        elif name == "sunduk":
            self.image = pygame.transform.scale(self.image, (130, 100))
            self.rect = self.image.get_rect()
            self.rect = self.rect.move(x, 360)
        elif name == "npc":
            self.image = pygame.transform.scale(self.image, (280, 300))
            self.rect = self.image.get_rect()
            self.rect = self.rect.move(x, 200)
        elif name == "fair":
            self.image = pygame.transform.scale(self.image, (100, 100))
            self.rect = self.image.get_rect()
            self.rect = self.rect.move(x, 400)


class Boots(pygame.sprite.Sprite):
    image = load_image("boots.png")

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Boots.image
        self.image = pygame.transform.scale(self.image, (150, 200))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = -50


class Bag(pygame.sprite.Sprite):
    image = load_image("boybag.png")

    def __init__(self, y):
        super().__init__(all_sprites)
        self.image = Bag.image
        self.image = pygame.transform.scale(self.image, (180, 230))
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = y


class Ball(pygame.sprite.Sprite):
    image = load_image("ball.png")

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = Ball.image
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Sunduk(pygame.sprite.Sprite):
    image = load_image("sunduk.png")
    image1 = load_image("sundukpaint.png")

    def __init__(self, image, x):
        super().__init__(all_sprites)
        self.image = image
        self.image = pygame.transform.scale(self.image, (130, 100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 20


def update(sunduk):
    floor = Floor()
    Background(0)
    Background(400)
    Background(800)
    x = 0
    for i in range(3):
        floor_up = FloorUp(x)
        x += 400
    Boots()
    if sunduk == 0:
        Sunduk(load_image("sundukpaint.png"), 760)
        Sunduk(load_image("sundukpaint.png"), 910)
        Sunduk(load_image("sundukpaint.png"), 1060)
    if sunduk == 1:
        Sunduk(load_image("sunduk.png"), 760)
        Sunduk(load_image("sundukpaint.png"), 910)
        Sunduk(load_image("sundukpaint.png"), 1060)
    if sunduk == 2:
        Sunduk(load_image("sunduk.png"), 760)
        Sunduk(load_image("sunduk.png"), 910)
        Sunduk(load_image("sundukpaint.png"), 1060)
    if sunduk >= 3:
        Sunduk(load_image("sunduk.png"), 760)
        Sunduk(load_image("sunduk.png"), 910)
        Sunduk(load_image("sunduk.png"), 1060)


def text(n):
    font = pygame.font.Font(None, 100)
    text = font.render(str(n), True, (0, 255, 0))
    text_x = 160
    text_y = 25
    screen.blit(text, (text_x, text_y))


start_window(width, height)
sunduk = 0
update(sunduk)
BOY = [load_image("boy1.png"), load_image("boy5.png"), load_image("boy2.png"), load_image("boy3.png"), load_image("boy4.png")]
BOY_NIKE = [load_image("boynike1.png"), load_image("boynike5.png"), load_image("boynike2.png"), load_image("boynike3.png"), load_image("boynike4.png")]

time = 0
Start(load_image("boy1.png"))
CHOOSE = ["stone", "npc", "boots", "bag", "stone", "npc", "stone", "stone", "stone", "stone", "stone", "sunduk"]
y = 275
x1 = 1200
k1 = 0
boy_bag = 0
k2 = 0
st = randint(10, 50)
sub = 11
choose_subject = CHOOSE[randint(0, sub)]
st_list = []
amount_boots = 0
seconds_boots = 1000
npc_list = ["npc.png", "npc1.png", "npc2.png"]
balls = []
drop_ball = False
draw = False
jump_time = 0
bag_y = 230
running = True
boots_jump = False
draw_bag = False
jump = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            draw = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if not draw_bag:
                jump = True
                draw = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            if not draw_bag:
                if amount_boots != 0:
                    amount_boots -= 1
                    seconds_boots = 0
                else:
                    amount_boots = 0
                    seconds_boots = 1000
            jump_time = 0
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            Ball(375, y + 75)
            balls.append([375, y + 75])
            drop_ball = True
    st_list = list(filter(lambda x: x[2] > 0, st_list))
    balls = list(filter(lambda x: x[0] < width, balls))
    if jump:
        if seconds_boots > 100:
            Start(load_image("boy5.png"))
            for all in all_sprites:
                all.kill()
            update(sunduk)
            y -= 50
            jump = Jump(load_image("boy4.png"), y)
            for i in range(len(balls)):
                balls[i][0] += 20
                ball = Ball(balls[i][0], balls[i][1])
            for i in range(len(st_list)):
                st_list[i][2] = st_list[i][2] - 100
                stone = Subject(st_list[i][0], st_list[i][1], st_list[i][2])
                if st_list[i][0] == "npc":
                    x5 = stone.rect.x
                    y5 = stone.rect.y
                    w5 = stone.rect.width
                    h5 = stone.rect.height
                    for j in range(len(balls)):
                        n = [balls[j][0], balls[j][1], 50, 50]
                        m = [x5, y5, w5, h5]
                        if not(n[0] + n[2] < m[0] or m[0] + m[2] < n[0] or n[1] + n[3] < m[1] or m[1] + m[3] < n[1]):
                            st_list[i][0] = "fair"
                            st_list[i][1] = load_image("ball2.PNG")
                            if len(balls) != 0:
                                del balls[j]
                            jump_time = 0
                            break
                if jump.rect.colliderect(stone.rect):
                    if st_list[i][0] == "stone":
                        draw = False
                        jump_time = 0
                    if st_list[i][0] == "npc":
                        draw = False
                        jump = False
                        draw_bag = False
                        jump_time = 0
                    if st_list[i][0] == "boots":
                        amount_boots += 1
                        st_list[i][2] = -1
                    if st_list[i][0] == "sunduk":
                        sunduk += 1
                        if sunduk == 3 and k2 == 0:
                            k2 = 1
                            sub -= 1
                        st_list[i][2] = -1
                    if st_list[i][0] == "bag":
                        st_list[i][2] = -200
                        seconds_boots = 1000
                        draw = False
                        jump = False
                        draw_bag = True
            if y < 100:
                y = 250
                time = 3
                jump = False
                draw = True
            seconds_boots += 1
        else:
            Start(load_image("boynike5.png"))
            for all in all_sprites:
                all.kill()
            update(sunduk)
            if jump_time == 0:
                y -= 50
            else:
                y += 50
            jump = Jump(load_image("boynike2.png"), y)
            for i in range(len(balls)):
                balls[i][0] += 20
                ball = Ball(balls[i][0], balls[i][1])
            for i in range(len(st_list)):
                st_list[i][2] = st_list[i][2] - 100
                stone = Subject(st_list[i][0], st_list[i][1], st_list[i][2])
                if st_list[i][0] == "npc":
                    x5 = stone.rect.x
                    y5 = stone.rect.y
                    w5 = stone.rect.width
                    h5 = stone.rect.height
                    for j in range(len(balls)):
                        n = [balls[j][0], balls[j][1], 50, 50]
                        m = [x5, y5, w5, h5]
                        if not (n[0] + n[2] < m[0] or m[0] + m[2] < n[0] or n[1] + n[3] < m[1] or m[1] + m[3] < n[1]):
                            st_list[i][0] = "fair"
                            st_list[i][1] = load_image("ball2.PNG")
                            if len(balls) != 0:
                                del balls[j]
                            jump_time = 0
                            break
                if jump.rect.colliderect(stone.rect):
                    if st_list[i][0] == "stone":
                        draw = False
                        jump_time = 0
                    if st_list[i][0] == "npc":
                        draw = False
                        jump = False
                        draw_bag = False
                        jump_time = 0
                    if st_list[i][0] == "boots":
                        amount_boots += 1
                        st_list[i][2] = -1
                    if st_list[i][0] == "sunduk":
                        sunduk += 1
                        if sunduk == 3 and k2 == 0:
                            k2 = 1
                            sub -= 1
                        st_list[i][2] = -1
                    if st_list[i][0] == "bag":
                        st_list[i][2] = -200
                        seconds_boots = 1000
                        draw = False
                        jump = False
                        draw_bag = True
                        jump_time = 0
            if y < 0:
                jump_time = 1
            if jump_time == 1 and y == 250:
                jump_time = 0
                time = 3
                jump = False
                draw = True
            seconds_boots += 1
    if draw:
        jump_time = 0
        for all in all_sprites:
            all.kill()
        update(sunduk)
        if k1 == st:
            k1 = 0
            if choose_subject == "stone":
                stone = Subject("stone", load_image("stone.PNG"), 1200)
                st_list.append(["stone", load_image("stone.PNG"), 1200])
            if choose_subject == "boots":
                stone = Subject("boots", load_image("boots.PNG"), 1200)
                st_list.append(["boots", load_image("boots.PNG"), 1200])
            if choose_subject == "bag":
                stone = Subject("bag", load_image("bag.PNG"), 1200)
                st_list.append(["bag", load_image("bag.PNG"), 1200])
            if choose_subject == "sunduk":
                stone = Subject("sunduk", load_image("sunduk.PNG"), 1200)
                st_list.append(["sunduk", load_image("sunduk.PNG"), 1200])
            if choose_subject == "npc":
                n = choice(npc_list)
                stone = Subject("npc", load_image(n), 1200)
                st_list.append(["npc", load_image(n), 1200])
            if sunduk == 3 and k2 == 0:
                k2 = 1
                sub -= 1
            st = randint(10, 30)
            choose_subject = CHOOSE[randint(0, sub)]
        if seconds_boots > 100:
            run = Run(BOY[time % len(BOY)])
        else:
            run = Run(BOY_NIKE[time % len(BOY)])
        for i in range(len(balls)):
            balls[i][0] += 20
            ball = Ball(balls[i][0], balls[i][1])
        for i in range(len(st_list)):
            st_list[i][2] = st_list[i][2] - 50
            stone = Subject(st_list[i][0], st_list[i][1], st_list[i][2])
            if st_list[i][0] == "npc":
                x5 = stone.rect.x
                y5 = stone.rect.y
                w5 = stone.rect.width
                h5 = stone.rect.height
                for j in range(len(balls)):
                    n = [balls[j][0], balls[j][1], 50, 50]
                    m = [x5, y5, w5, h5]
                    if not (n[0] + n[2] < m[0] or m[0] + m[2] < n[0] or n[1] + n[3] < m[1] or m[1] + m[3] < n[1]):
                        st_list[i][0] = "fair"
                        st_list[i][1] = load_image("ball2.PNG")
                        if len(balls) != 0:
                            del balls[j]
                        break
            if run.rect.colliderect(stone.rect):
                if st_list[i][0] == "stone":
                    draw = False
                    jump_time = 0
                if st_list[i][0] == "npc" and drop_ball:
                    draw = False
                    jump = False
                    draw_bag = False
                    jump_time = 0
                if st_list[i][0] == "boots":
                    amount_boots += 1
                    st_list[i][2] = -1
                if st_list[i][0] == "sunduk":
                    sunduk += 1
                    if sunduk == 3 and k2 == 0:
                        k2 = 1
                        sub -= 1
                    st_list[i][2] = -1
                if st_list[i][0] == "bag":
                    st_list[i][2] = -200
                    seconds_boots = 1000
                    draw = False
                    jump = False
                    draw_bag = True
                    jump_time = 0

        time += 1
        k1 += 1
        seconds_boots += 1
    if draw_bag:
        jump_time = 0
        for all in all_sprites:
            all.kill()
        update(sunduk)
        if k1 == st:
            k1 = 0
            if choose_subject == "stone":
                stone = Subject("stone", load_image("stone.PNG"), 1200)
                st_list.append(["stone", load_image("stone.PNG"), 1200])
            if choose_subject == "boots":
                stone = Subject("boots", load_image("boots.PNG"), 1200)
                st_list.append(["boots", load_image("boots.PNG"), 1200])
            if choose_subject == "bag":
                stone = Subject("bag", load_image("bag.PNG"), 1200)
                st_list.append(["bag", load_image("bag.PNG"), 1200])
            if choose_subject == "sunduk":
                stone = Subject("sunduk", load_image("sunduk.PNG"), 1200)
                st_list.append(["sunduk", load_image("sunduk.PNG"), 1200])
            if choose_subject == "npc":
                n = choice(npc_list)
                stone = Subject("npc", load_image(n), 1200)
                st_list.append(["npc", load_image(n), 1200])
            if sunduk == 3 and k2 == 0:
                k2 = 1
                sub -= 1
            st = randint(50, 60)
            choose_subject = CHOOSE[randint(0, sub)]
        if y != 10:
            y -= 10
            run = Bag(y)
        else:
            run = Bag(10)
        for i in range(len(balls)):
            balls[i][0] += 10
            Ball(balls[i][0], balls[i][1])
        for i in range(len(st_list)):
            st_list[i][2] = st_list[i][2] - 50
            stone = Subject(st_list[i][0], st_list[i][1], st_list[i][2])

        time += 1
        k1 += 1
        seconds_boots += 1
        boy_bag += 1
        if boy_bag == 50:
            jump_time = 0
            y = 270
            boy_bag = 0
            draw_bag = False
            draw = True
    seconds_boots += 1
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    all_sprites.update()
    text(f"x {amount_boots}")
    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()
