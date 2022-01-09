import pygame
import os
import sys


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


class Pause:
    def __init__(self, width, height):
        self.image = pygame.transform.scale(load_image('Pause.png'), (width, height))
        self.transparency = 0
        self.move = 3.5
        self.width, self.height = width, height

    def update(self, time_delta, screen, manager2):
        manager2.update(time_delta)
        screen.blit(self.image, (0, 0))
        font = pygame.font.Font(None, 100)
        text = font.render("Pause", True, "white")
        text_x = self.width // 2 - text.get_width() // 2
        text_y = (self.height // 2 - text.get_height() // 2) * 0.5
        text.set_alpha(self.transparency)
        screen.blit(text, (text_x, text_y))
        manager2.draw_ui(screen)
        self.transparency += self.move
        if not(0 < self.transparency < 300):
            self.move = -self.move