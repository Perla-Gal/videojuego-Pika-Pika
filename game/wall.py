from turtle import left
import pygame
from .config import *

#Crear OBSTÁCULOS con clase Wall
class Wall (pygame.sprite.Sprite):  #hereda de pygame 

    def __init__(self, left, bottom):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((40, 80))  #superficie del obstaculo como pared
        self.image.fill(RED)

        self.rect = self.image.get_rect()  #Rectangulo
        self.rect.left = left
        self.rect.bottom = bottom
        self.vel_x = SPEED

        self.rect_top = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, 1)

    def update(self):
        self.rect.left -= self.vel_x

        self.rect_top.x = self.rect.x

    def stop(self):
        self.vel_x = 0




        
