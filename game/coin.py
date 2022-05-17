import pygame
import os

from .config import *

#CREA LA MONEDA 
class Coin(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, dir_images):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(os.path.join(dir_images, "POKEBALL.png"))
        self.image = pygame.transform.scale(self.image, (40, 40))

        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

        self.vel_x = SPEED
    
    def update(self):
        self.rect.left -= self.vel_x

    def stop(self):
        self.vel_x = 0