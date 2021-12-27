import pygame
import zipfile
import os
import pygame_gui

# Инициализация
pygame.init()
size = width, height = 1000, 650
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Начало')
screen.fill((0, 0, 0))
LANGUAGE = 'Русский'

# Открытие файла с картинками для заставки
fname = os.path.join(os.getcwd(), 'data', 'Snow.zip')
directory = os.path.join(os.getcwd(), 'data')
with zipfile.ZipFile(fname, "r") as f:
    names = f.namelist()
    f.extractall(directory)


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


def draw_name():
    font = pygame.font.Font(None, 85)
    text = font.render("Однажды в Рождество" * (LANGUAGE == 'Русский') +
                       "One Christmas Eve" * (LANGUAGE == 'English'), True, "#84DFFF")
    text_x = width // 2 - text.get_width() // 2
    text_y = (height // 2 - text.get_height() // 2) // 2
    screen.blit(text, (text_x, text_y))


# Настройка кнопок
manager = pygame_gui.UIManager((width, height))
main_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(((width - 100) // 2, (height - 50) / 2, 100, 50)),
    text='Начать игру' * (LANGUAGE == 'Русский') + "Start" * (LANGUAGE == 'English'),
    manager=manager
)
choose_language = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
    options_list=['Русский', 'English'], starting_option='Русский',
    relative_rect=pygame.Rect(900, 582, 100, 25), manager=manager
)

# Музыка
sound_main_button = pygame.mixer.Sound(os.path.join(directory, 'Start game.wav'))
window_sound = pygame.mixer.Sound(os.path.join(directory, 'Main window music.mp3'))
window_sound.play(-1)

i = 0
running = True
clock = pygame.time.Clock()
while running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                LANGUAGE = event.text
                main_button.kill()
                main_button = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect(((width - 100) // 2, (height - 50) / 2, 100, 50)),
                    text='Начать игру' * (LANGUAGE == 'Русский') + "Start" * (
                                LANGUAGE == 'English'),
                    manager=manager
                )
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == main_button:
                    window_sound.stop()
                    sound_main_button.play()
        manager.process_events(event)
    manager.update(time_delta)
    BackGround = Background(os.path.join(directory, names[i]), [0, 0])
    i += 1
    if i == len(names):
        i = 0
    screen.fill([255, 255, 255])
    screen.blit(BackGround.image, BackGround.rect)
    draw_name()
    manager.draw_ui(screen)
    pygame.display.flip()
    clock.tick(30)
pygame.quit()

for name in names:
    os.remove(os.path.join(directory, name))