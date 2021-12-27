import pygame
import pygame_gui
import sys
import os
import zipfile
from Game_Over import GameOver

pygame.init()
size = width, height = 1000, 650
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Пасхалка')
screen.fill((0, 0, 0))
image = pygame.Surface([100, 100])
image.fill(pygame.Color('red'))

fname = os.path.join(os.getcwd(), 'data', 'CUPCAKE Jumpscare.zip')
directory = os.path.join(os.getcwd(), 'data')
with zipfile.ZipFile(fname, "r") as f:
    names = f.namelist()
    f.extractall(directory)


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


class Cupcake(pygame.sprite.Sprite):
    image1 = load_image("GoldenCupcake.png")
    image2 = load_image("CupcakeNormal.png")
    image3 = load_image("NightmareCupcake.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Cupcake.image1
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.now = 0

    def update(self):
        global end
        self.now += 1
        if self.now == 1:
            sound_error.play()
            self.image = Cupcake.image2
        if self.now == 2:
            sound_error.play()
            self.image = Cupcake.image3
        if self.now == 3:
            screamer.play()
            end = True
        self.rect = self.image.get_rect()


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


def draw_name():
    font = pygame.font.Font(None, 25)
    text = font.render("Year", True, "#6f6b00")
    text_x = (width // 2 - text.get_width() // 2) * 1.5
    text_y = (height // 2 - text.get_height() // 2) // 2
    screen.blit(text, (text_x, text_y))


def draw_code():
    font = pygame.font.Font(None, 85)
    text = font.render(line, True, "#a00dc7")
    text_x = (width // 2 - text.get_width() // 2) * 1.55
    text_y = (height // 2 - text.get_height() // 2) // 2 * 1.3
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, '#470000', (text_x - 10, text_y - 10,
                                           text_w + 20, text_h + 20), 1)


manager = pygame_gui.UIManager((width, height))
manager1 = pygame_gui.UIManager((width, height))
button1 = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((630, 260, 70, 50)),
    text='1',
    manager=manager
)
button2 = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((705, 260, 70, 50)),
    text='2',
    manager=manager
)
button3 = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((780, 260, 70, 50)),
    text='3',
    manager=manager
)

button4 = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((630, 315, 70, 50)),
    text='4',
    manager=manager
)
button5 = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((705, 315, 70, 50)),
    text='5',
    manager=manager
)
button6 = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((780, 315, 70, 50)),
    text='6',
    manager=manager
)

button7 = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((630, 370, 70, 50)),
    text='7',
    manager=manager
)
button8 = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((705, 370, 70, 50)),
    text='8',
    manager=manager
)
button9 = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((780, 370, 70, 50)),
    text='9',
    manager=manager
)

buttondel = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((630, 425, 70, 50)),
    text='Del',
    manager=manager
)
button0 = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((705, 425, 70, 50)),
    text='0',
    manager=manager
)
buttonok = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((780, 425, 70, 50)),
    text='OK',
    manager=manager
)
button_back_main_window = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((400, 355, 200, 50)),
    text='На главный экран',
    manager=manager1
)
button_last_save = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((400, 300, 200, 50)),
    text='К последнему сохранению',
    manager=manager1
)

directory = os.path.join(os.getcwd(), 'data')
start_attention = pygame.mixer.Sound(os.path.join(directory, 'Windowscare.mp3'))
start_attention.play()
sound_error = pygame.mixer.Sound(os.path.join(directory, 'Error.mp3'))
screamer = pygame.mixer.Sound(os.path.join(directory, 'CUPCAKE Jumpscare audio.wav'))

all_sprites = pygame.sprite.Group()
cupcake = Cupcake(all_sprites)
line = ''
running = True
end = False
i = 0
game_over = False
end_screen = GameOver(width, height)
clock = pygame.time.Clock()
while running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element in (button1, button2, button3, button4, button5, button6,
                                        button7, button8, button9, button0):
                    line += event.ui_element.text
                if event.ui_element == buttondel:
                    if line != '':
                        line = line[:-1]
                if event.ui_element == buttonok:
                    if line != '2014':
                        cupcake.update()
                        line = ''
                    else:
                        print('OK')
                if event.ui_element in (button_back_main_window, button_last_save):
                    print('Back')
        manager.process_events(event)
        manager1.process_events(event)
    if not end:
        manager.update(time_delta)
        screen.fill('black')
        all_sprites.draw(screen)
        draw_name()
        if line != '':
            draw_code()
        manager.draw_ui(screen)
    elif not game_over:
        BackGround = Background(os.path.join(directory, names[i]), [0, 0])
        screen.fill([255, 255, 255])
        screen.blit(BackGround.image, BackGround.rect)
        i += 1
        if i == len(names):
            game_over = True
    else:
        end_screen.update(time_delta, screen, manager1)
    pygame.display.flip()
pygame.quit()

for name in names:
    os.remove(os.path.join(directory, name))