import pygame
import sys
import os

pygame.init()
size = width, height = 1000, 650
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Уровень')
screen.fill((0, 0, 0))
FPS = 50
clock = pygame.time.Clock()


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


walkLeft = [load_image('R1.png'), load_image('R2.png'), load_image('R3.png'),
            load_image('R4.png'), load_image('R5.png'), load_image('R6.png'),
            load_image('R7.png'), load_image('R8.png'), load_image('R9.png'),
            load_image('R10.png')]
walkRight = [pygame.transform.flip(load_image('R1.png'), 90, 0),
             pygame.transform.flip(load_image('R2.png'), 90, 0),
             pygame.transform.flip(load_image('R3.png'), 90, 0),
             pygame.transform.flip(load_image('R4.png'), 90, 0),
             pygame.transform.flip(load_image('R5.png'), 90, 0),
             pygame.transform.flip(load_image('R6.png'), 90, 0),
             pygame.transform.flip(load_image('R7.png'), 90, 0),
             pygame.transform.flip(load_image('R8.png'), 90, 0),
             pygame.transform.flip(load_image('R9.png'), 90, 0),
             pygame.transform.flip(load_image('R10.png'), 90, 0)]
jumpLeft = [load_image('J1.png'), load_image('J2.png'), load_image('J3.png'),
            load_image('J4.png'), load_image('J5.png'), load_image('J6.png'),
            load_image('J7.png'), load_image('J8.png'), load_image('J9.png'),
            load_image('J10.png')]
jumpRight = [pygame.transform.flip(load_image('J1.png'), 90, 0),
             pygame.transform.flip(load_image('J2.png'), 90, 0),
             pygame.transform.flip(load_image('J3.png'), 90, 0),
             pygame.transform.flip(load_image('J4.png'), 90, 0),
             pygame.transform.flip(load_image('J5.png'), 90, 0),
             pygame.transform.flip(load_image('J6.png'), 90, 0),
             pygame.transform.flip(load_image('J7.png'), 90, 0),
             pygame.transform.flip(load_image('J8.png'), 90, 0),
             pygame.transform.flip(load_image('J9.png'), 90, 0),
             pygame.transform.flip(load_image('J10.png'), 90, 0)]
bg = load_image('bg.jpg')
char = pygame.transform.flip(load_image('R1.png'), 90, 0)

isJump = False
jumpCount = 10

left = False
right = False
walkCount = 0


class GoLeft(pygame.sprite.Sprite):
    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.i = 0
        self.image = pygame.transform.scale(walkLeft[0], (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.i += 1
        if self.i == len(walkLeft):
            self.i = 0
        self.image = pygame.transform.scale(walkLeft[self.i], (100, 100))
        self.rect.move(-3, 0)
        self.rect.x -= 3
        return self.rect.x, self.rect.y

    def stay(self):
        self.i = 0
        self.image = pygame.transform.scale(walkLeft[self.i], (100, 100))


class GoRight(pygame.sprite.Sprite):
    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.i = 0
        self.image = pygame.transform.scale(walkRight[0], (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.i += 1
        if self.i == len(walkRight):
            self.i = 0
        self.image = pygame.transform.scale(walkRight[self.i], (100, 100))
        self.rect.move(3, 0)
        self.rect.x += 3
        return self.rect.x, self.rect.y

    def stay(self):
        self.i = 0
        self.image = pygame.transform.scale(walkRight[self.i], (100, 100))


class Jump(pygame.sprite.Sprite):
    def __init__(self, x, y, where, *group):
        super().__init__(*group)
        self.i = 0
        if where in ('right', 'No'):
            self.image = pygame.transform.scale(jumpRight[self.i], (100, 100))
        else:
            self.image = pygame.transform.scale(jumpLeft[self.i], (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move = 1

    def update(self, where):
        self.i += 1
        if self.i == len(walkRight):
            self.i = 0
        if where in ('right', 'No'):
            self.image = pygame.transform.scale(jumpRight[self.i], (100, 100))
        else:
            self.image = pygame.transform.scale(jumpLeft[self.i], (100, 100))
        if where == 'No':
            self.rect.move(0, -(jumpCount * abs(jumpCount)) * 0.5)
            self.rect.y += -(jumpCount * abs(jumpCount)) * 0.5
        elif where == 'right':
            self.rect.move(3, -(jumpCount * abs(jumpCount)) * 0.5)
            self.rect.x += 3
            self.rect.y += -(jumpCount * abs(jumpCount)) * 0.5
        else:
            self.rect.move(-3, -(jumpCount * abs(jumpCount)) * 0.5)
            self.rect.x -= 3
            self.rect.y += -(jumpCount * abs(jumpCount)) * 0.5
        if self.rect.y > 550:
            self.rect.y = 550
        return self.rect.x, self.rect.y


all_sprites = pygame.sprite.Group()
x, y = 500, 550
hero_go_left = 0
hero_go_right = GoRight(x, y, all_sprites)
hero_jump = 0
jump_where = 'right'
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if isJump:
            jump_where = 'left'
        else:
            if hero_go_left == 0:
                jump_where = 'left'
                all_sprites = pygame.sprite.Group()
                hero_go_right = 0
                hero_stay = 0
                hero_go_left = GoLeft(x, y, all_sprites)
            x, y = hero_go_left.update()
    elif keys[pygame.K_RIGHT]:
        if isJump:
            jump_where = 'right'
        else:
            if hero_go_right == 0:
                jump_where = 'right'
                all_sprites = pygame.sprite.Group()
                hero_go_left = 0
                hero_stay = 0
                hero_go_right = GoRight(x, y, all_sprites)
            x, y = hero_go_right.update()
    else:
        if not isJump:
            jump_where = 'No'
            if hero_go_left == 0:
                hero_go_right.stay()
            if hero_go_right == 0:
                hero_go_left.stay()
    if not isJump:
        if keys[pygame.K_SPACE]:
            isJump = True
            all_sprites = pygame.sprite.Group()
            hero_jump = Jump(x, y, jump_where, all_sprites)
            x,y = hero_jump.update(jump_where)
    else:
        if jumpCount >= -10:
            jumpCount -= 1
            x, y = hero_jump.update(jump_where)
        else:
            jumpCount = 10
            isJump = False
            hero_jump = 0
            all_sprites = pygame.sprite.Group()
            if jump_where in ('right', 'No'):
                hero_go_right = GoRight(x, y, all_sprites)
                hero_go_left = 0
            else:
                hero_go_left = GoLeft(x, y, all_sprites)
                hero_go_right = 0
    all_sprites.draw(screen)
    pygame.display.flip()
    screen.blit(bg, (0, 0))
    clock.tick(FPS)
pygame.quit()