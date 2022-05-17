import pygame
from .config import *

#Crear plataforma con su clase Platform
class Platform(pygame.sprite.Sprite):  
    def __init__(self):  
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((WIDTH, 40)) #Generar la superficie 
        self.image.fill(GREEN)  #Pintamos la superficie 

        self.rect = self.image.get_rect ()
        self.rect.x = 0
        self.rect.y = HEIGHT - 40
       

